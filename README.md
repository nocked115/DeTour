# DeTOUR

다비(DAVI) 프로젝트의 웹/와이어프레임 작업 공간입니다.

## 현재 구성

- `detour-landing.html` — 랜딩 페이지 시안
- `DETOUR_PROJECT_SPEC.md` — 프로젝트 명세
- `DETOUR_5WEEK_HANDOFF.md` — 작업 인수인계 문서

## 개발 환경

현재는 별도 빌드 도구 없이 정적 HTML로 시작합니다. `detour-landing.html`을 브라우저에서 열어 확인할 수 있습니다.

## GitHub 연결

로컬 저장소를 초기화한 뒤 GitHub 저장소를 remote로 등록합니다.

```bash
git remote add origin <GITHUB_REPOSITORY_URL>
git add .
git commit -m "chore: initialize project workspace"
git branch -M main
git push -u origin main
```

