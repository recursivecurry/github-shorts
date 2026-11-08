# github-shorts

GitHub PR을 세로형 설명 영상으로 보고, 퀴즈를 맞힌 뒤 리뷰하는 웹서비스다.

에이전트는 서버 옵션에서 Claude Code CLI(기본값) 또는 Codex CLI를 선택하도록 설계한다. 선택한 에이전트가 PR 분석과 설명·퀴즈·영상 생성을 모두 처리한다.

## 개발 문서

- [Requirement.md](Requirement.md): 확정된 제품 요구사항과 인수 기준을 정의한다.
- [Design.md](Design.md): GitHub 연동, 생성·서빙, 퀴즈·리뷰와 삭제 흐름을 설계한다.
- [UI-Figma.md](UI-Figma.md): 화면별 동작과 [Figma UI 문서](https://www.figma.com/design/oMPbx1zq40HVZirA1CzJmu)를 연결한다.
- [TODO.md](TODO.md): 개발 순서와 단계별 할 일·완료 기준을 관리한다.

현재는 요구사항과 설계를 작성하는 단계이며, 실행 가능한 서비스는 아직 구현하지 않았다.
