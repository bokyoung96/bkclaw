# Playwright MCP Usage

## Purpose

Playwright MCP는 브라우저 자동화가 실제로 필요한 작업에서만 승격하는 optional capability다.
기본 검색/문서 fetch는 기존 lightweight 경로를 우선한다.

## Default posture

기본은 아래 도구를 우선한다.
1. web fetch / search
2. Tavily
3. local/runtime helpers

아래일 때만 Playwright MCP를 검토한다.
- 동적 렌더링
- 클릭/스크롤/탭 전환 필요
- 시각/브라우저 상 실제 동작 검증 필요
- fetch/search만으로 부족

## Config

Example MCP config:
- `configs/mcp/playwright.mcp.json`

Standard shape:
```json
{
  "mcpServers": {
    "playwright": {
      "command": "npx",
      "args": ["-y", "@playwright/mcp@latest"]
    }
  }
}
```

## Preflight

Before relying on Playwright MCP:
1. `node --version`
2. `npm --version`
3. `./bin/check_playwright_mcp`
4. if needed, browser runtime install/check

Preferred smoke path in this repo currently uses `pnpm dlx` rather than `npx`, because the current runtime showed npm/npx cache-lock instability.

## Use when

- 브라우저 기반 검증이 실제 가치가 있을 때
- MCP의 지속 state / page context가 필요한 작업
- exploratory automation 또는 self-healing style browser loop가 필요한 경우

## Avoid when

- 단순 웹 문서 fetch
- 정적 페이지 읽기
- 짧은 리서치 질의
- 브라우저 없이도 결과가 충분한 경우
