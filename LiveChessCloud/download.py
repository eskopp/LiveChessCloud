from typing import Optional, Dict, AsyncIterator, List, Tuple, Any
import logging
import aiohttp
from urllib.parse import urlparse, urlencode
from urllib.request import Request, urlopen
import json
import re
import chess
from datetime import datetime
import asyncio

# Constants
BOARD_CHESS, BOARD_DRAUGHTS, BOARD_GO, BOARD_MILL = range(4)
BOARDS_DESC = ["Chess", "Draughts", "Go", "Mill"]
METHOD_DL, METHOD_HTML, METHOD_API, METHOD_MISC, METHOD_WS = range(5)
METHODS_DESC = [
    "Download link",
    "HTML parsing",
    "Application programming interface",
    "Various techniques",
    "Websockets",
]
(
    TYPE_GAME,
    TYPE_STUDY,
    TYPE_PUZZLE,
    TYPE_SWISS,
    TYPE_TOURNAMENT,
    TYPE_EVENT,
    TYPE_FEN,
) = range(7)

# Constants
CHESS960 = "Fischerandom"
CHESS960_CLASSICAL = 518
FEN_START = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
FEN_START_960 = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w HAha - 0 1"


class InternetWebsockets:
    def __init__(self):
        self.acs: Optional[aiohttp.ClientSession] = None
        self.ws: Optional[aiohttp.client_ws.ClientWebSocketResponse] = None

    async def connect(
        self, url: Optional[str], headers: Optional[Dict] = None
    ) -> "InternetWebsockets":
        if url is not None:
            logging.debug("Websocket connecting to %s", url)
            self.acs = aiohttp.ClientSession()
            self.ws = await self.acs.ws_connect(url, headers=headers, heartbeat=None)
        return self

    async def recv(self) -> AsyncIterator[Optional[str]]:
        result = None
        if self.ws is not None:
            async for msg in self.ws:
                if msg.type == aiohttp.WSMsgType.TEXT:
                    result = msg.data
                break
        yield result

    async def send(self, data: str) -> None:
        if self.ws is not None:
            await self.ws.send_str(data)

    async def close(self) -> None:
        if self.ws is not None:
            await self.ws.close()
            self.ws = None
        if self.acs is not None:
            await self.acs.close()
            self.acs = None


class InternetGameInterface:
    def __init__(self):
        self.user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
        self.id: Optional[str] = None
        self.regexes: Dict[str, Any] = {}

    def send_xhr(
        self, url: Optional[str], postData: Optional[Dict], origin: Optional[str] = None
    ) -> Optional[str]:
        """Call a target URL by submitting the POSTDATA.
        The value None is returned in case of error."""
        # Check
        if url in [None, ""]:
            return None

        # Call data
        if postData is not None:
            data: Optional[bytes] = urlencode(postData).encode()
        else:
            data = None
        try:
            logging.debug("Calling API: %s", url)
            headers = {
                "User-Agent": self.user_agent,
                "Accept": "application/json, text/plain, */*",
            }
            if origin is not None:
                headers["Origin"] = origin
            with urlopen(Request(str(url), data, headers=headers)) as response:
                respdata = self.read_data(response)
            return respdata
        except Exception as exception:
            logging.debug("Exception raised: %s", str(exception))
            return None

    def json_loads(self, data: Optional[str]) -> Optional[Dict]:
        """Load a JSON and handle the errors.
        The value None is returned when the data are not relevant or misbuilt."""
        try:
            if data in [None, ""]:
                return None
            return json.loads(str(data))
        except ValueError:
            return None

    def json_field(
        self,
        data: Optional[Dict],
        path: str,
        default: str = "",
        separator: str = "/",
    ) -> str:
        """Conveniently read a field from a JSON data. The PATH is a key like "node1/node2/key".
        A blank string is returned in case of error."""
        if data in [None, ""]:
            return ""
        keys = path.split(separator)
        value: Any = data
        for key in keys:
            if key == "*":
                value = list(value.keys())[0]
            elif key.startswith("[") and key.endswith("]"):
                try:
                    value = value[int(key[1:-1])]
                except (ValueError, TypeError, IndexError):
                    return ""
            elif (value is not None) and (key in value):
                value = value[key]
            else:
                return ""
        return default if value in [None, ""] else value

    def safe_int(self, value: Any) -> int:
        try:
            return int(value)
        except Exception:
            return 0

    def read_data(self, response):
        """Read the data from the URL request."""
        if (
            "Content-Encoding" in response.headers
            and response.headers["Content-Encoding"] == "gzip"
        ):
            data = zlib.decompress(response.read(), 16 + zlib.MAX_WBITS)
        else:
            data = response.read()
        return data.decode("utf-8")

    def assign_game(self, url: str) -> bool:
        pass

    def download_game(self) -> Optional[str]:
        pass

    def get_test_links(self) -> List[Tuple[str, bool]]:
        pass

    def get_identity(self) -> Tuple[str, int, int]:
        pass


class InternetGameLivechesscloud(InternetGameInterface):
    def __init__(self):
        InternetGameInterface.__init__(self)
        self.regexes.update({"id": re.compile(r"^[0-9a-f-]{36}$", re.IGNORECASE)})

    def get_identity(self) -> Tuple[str, int, int]:
        return "LiveChessCloud.com", BOARD_CHESS, METHOD_API

    def rebuild_pgn(self, game: Optional[Dict]) -> Optional[str]:
        """Return an object in PGN format.
        The keys starting with "_" are dropped silently.
        The key "_url" becomes the first comment.
        The key "_moves" contains the moves.
        The key "_reason" becomes the last comment."""
        # Check
        if (game is None) or (game == "") or (game.get("_moves", "") == ""):
            return None

        # Fix the tags
        if (
            "FEN" in game
        ):  # Convert Chess960 to classical chess depending on the start position
            if "Variant" in game:
                if game["Variant"] == CHESS960 and game["FEN"] == FEN_START_960:
                    del game["Variant"], game["SetUp"], game["FEN"]
            else:
                if game["FEN"] == FEN_START:
                    del game["SetUp"], game["FEN"]
        if "Result" in game:  # Special signs
            game["Result"] = game["Result"].replace("½", "1/2")

        # Header
        pgn = self.build_header(game)

        # Body
        def _inline_tag(key, mask):
            nonlocal pgn
            if (key in game) and (str(game[key]).strip() != ""):
                pgn += mask % str(game[key]).strip()

        _inline_tag("_url", "{%s}\n")
        _inline_tag("_moves", "%s ")
        _inline_tag("_reason", "{%s} ")
        _inline_tag("Result", "%s ")
        return pgn.strip()

    def build_header(self, game: Dict) -> str:
        pgn = ""
        roster = ["Event", "Site", "Date", "Round", "White", "Black", "Result"]
        if "Player3" in game:  # GreenChess
            roster.remove("White")
            roster.remove("Black")
        for e in list(game.keys()):
            if game[e] in [None, ""]:
                del game[e]
        for tag in roster:
            pgn += '[%s "%s"]\n' % (
                tag,
                str(game.get(tag, "????.??.??" if tag == "Date" else "?")).strip(),
            )
        for e in game:
            if (e not in roster) and (e[:1] != "_"):
                pgn += '[%s "%s"]\n' % (e, str(game[e]).strip())
        pgn += "\n"
        return pgn

    def assign_game(self, url: str) -> bool:
        # Verify the hostname
        parsed = urlparse(url)
        if parsed.netloc.lower() != "view.livechesscloud.com":
            return False

        # Verify the identifier
        gid = parsed.path[1:] or parsed.fragment
        if self.regexes["id"].match(gid) is not None:
            self.id = gid
            return True
        return False

    async def download_game(self) -> Optional[str]:
        # Check
        if self.id is None:
            return None

        # Fetch the host
        bourne = self.send_xhr("http://lookup.livechesscloud.com/meta/" + self.id, None)
        data = self.json_loads(bourne)
        host = self.json_field(data, "host")
        if host == "" or (self.json_field(data, "format") != "1"):
            return None

        # Fetch the tournament
        pgn = ""
        bourne = self.send_xhr(
            "http://%s/get/%s/tournament.json" % (host, self.id), None
        )
        data = self.json_loads(bourne)
        game = {
            "TimeControl": self.json_field(data, "timecontrol")
            .replace('"', "")
            .replace("'", ""),
            "Event": self.json_field(data, "name"),
            "Site": (
                "%s %s"
                % (self.json_field(data, "country"), self.json_field(data, "location"))
            ).strip(),
        }
        variant = self.json_field(data, "rules")
        if variant != "STANDARD":
            game["Variant"] = variant
        nb_rounds = len(self.json_field(data, "rounds", []))
        if nb_rounds == 0:
            return None

        # Fetch the rounds
        for i in range(1, nb_rounds + 1):
            bourne = self.send_xhr(
                "http://%s/get/%s/round-%d/index.json" % (host, self.id, i), None
            )
            data = self.json_loads(bourne)
            game_date = self.json_field(data, "date")
            pairings = self.json_field(data, "pairings", [])
            nb_pairings = len(pairings)
            if nb_pairings > 0:
                for j in range(nb_pairings):
                    # Players and result
                    player = pairings[j].get("white", {})
                    game["White"] = (
                        "%s, %s"
                        % (
                            self.json_field(player, "lname"),
                            self.json_field(player, "fname"),
                        )
                    ).strip()
                    player = pairings[j].get("black", {})
                    game["Black"] = (
                        "%s, %s"
                        % (
                            self.json_field(player, "lname"),
                            self.json_field(player, "fname"),
                        )
                    ).strip()
                    game["Result"] = self.json_field(pairings[j], "result", "*")
                    game["Round"] = "%d.%d" % (i, j + 1)

                    # Fetch the moves
                    game["_moves"] = ""
                    bourne2 = self.send_xhr(
                        "http://%s/get/%s/round-%d/game-%d.json?poll="
                        % (host, self.id, i, j + 1),
                        None,
                    )
                    data2 = self.json_loads(bourne2)
                    if self.json_field(data2, "result") == "NOTPLAYED":
                        continue
                    tstamp = self.safe_int(self.json_field(data2, "firstMove"))
                    game["Date"] = (
                        datetime.fromtimestamp(tstamp // 1000).strftime("%Y.%m.%d")
                        if tstamp > 0
                        else game_date
                    )
                    fischer_id = self.json_field(data2, "chess960", CHESS960_CLASSICAL)
                    if fischer_id == CHESS960_CLASSICAL:
                        for k in ["Variant", "SetUp", "FEN"]:
                            if k in game:
                                del game[k]
                    else:
                        game["Variant"] = CHESS960
                        game["SetUp"] = "1"
                        game["FEN"] = chess.Board.from_chess960_pos(fischer_id).fen()
                    game["_reason"] = self.json_field(data2, "comment")
                    moves = self.json_field(data2, "moves")
                    for move_number, move in enumerate(moves):
                        move = move.split(" ")[0]
                        if move_number % 2 == 0:
                            game["_moves"] += str(move_number // 2 + 1) + ". "
                        game["_moves"] += "%s " % move

                    # Game
                    candidate = self.rebuild_pgn(game)
                    if candidate is not None:
                        pgn += candidate.strip() + "\n\n"

        # Return the games
        return pgn

    def get_test_links(self) -> List[Tuple[str, bool]]:
        return [
            (
                "https://view.livechesscloud.com/30d54b79-e852-4788-bb91-403955efd6a3",
                True,
            ),  # Games
            (
                "https://view.livechesscloud.com/#30d54b79-e852-4788-bb91-403955efd6a3",
                True,
            ),  # Games, other scheme
            # No example found for Chess960
            ("http://view.livechesscloud.com", False),
        ]  # Not a game (homepage)


async def download(url: str) -> Optional[str]:
    internet_game = InternetGameLivechesscloud()
    if internet_game.assign_game(url):
        return await internet_game.download_game()
    else:
        return None


# Beispielaufruf
def download(url: str) -> Optional[str]:
    internet_game = InternetGameLivechesscloud()
    if internet_game.assign_game(url):
        return internet_game.download_game()
    else:
        return None


async def run_download(url: str) -> None:
    result = await download(url)
    result = (
        result.replace("ä", "ae")
        .replace("ö", "oe")
        .replace("ü", "ue")
        .replace("Ä", "Ae")
        .replace("Ö", "Oe")
        .replace("Ü", "Ue")
    )
    return result.replace("ß", "ss")
