"""환경 설정. API key는 .env에서만 읽고 코드에 적지 않는다."""
import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).parent.parent
load_dotenv(BASE_DIR / ".env")

KAKAO_REST_API_KEY = os.getenv("KAKAO_REST_API_KEY", "").strip()

# 브라우저에서 부를 수 있는 출처. 배포 주소를 여기에 둔다.
ALLOWED_ORIGINS = [
    "https://nocked115.github.io",
    "http://127.0.0.1:5500",
    "http://localhost:5500",
]

DATA_FILE = BASE_DIR / "data" / "places.json"


def kakao_ready() -> bool:
    """키가 있는지만 본다. 실제 사용 가능 여부는 호출해봐야 안다."""
    return bool(KAKAO_REST_API_KEY)
