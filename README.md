# Insight Feed 📰

컨설팅 리포트 & 아티클을 주제별로 매일 자동 수집하는 모바일 웹앱

**수집 출처**: McKinsey, BCG, HBR, Bain, Deloitte, Gartner  
**주제 분류**: AI / 금융 / IT / 컨설팅 / 정보보안 / 개인정보보호

---

## 🚀 설정 방법 (5단계)

### 1. GitHub 레포 생성
- GitHub에서 새 레포 생성 (Public 권장)
- 이 파일들 전부 push

### 2. GitHub Pages 설정
- 레포 → Settings → Pages
- Source: **Deploy from a branch**
- Branch: `main` / Folder: `/public`
- Save → 몇 분 후 `https://[유저명].github.io/[레포명]` 으로 접속 가능

### 3. GitHub Actions 권한 설정
- 레포 → Settings → Actions → General
- Workflow permissions: **Read and write permissions** 체크 → Save

### 4. 첫 번째 수동 실행
- 레포 → Actions → "Fetch RSS Articles" → Run workflow
- 완료되면 `public/articles.json` 자동 생성됨

### 5. 폰 홈화면에 추가 (PWA처럼)
- 폰 브라우저에서 사이트 접속
- 공유 버튼 → "홈 화면에 추가"
- 앱처럼 사용 가능 ✅

---

## ⚙️ 커스터마이징

### RSS 소스 추가/제거
`config.json` → `sources` 배열 편집

### 키워드 추가
`config.json` → `topics` 객체에서 각 주제별 키워드 배열 편집

### 수집 시간 변경
`.github/workflows/fetch.yml` → `cron` 값 변경  
현재: `0 21 * * *` = 매일 오전 6시 KST

---

## 📁 파일 구조

```
├── config.json                   # RSS 소스 & 키워드 설정
├── scripts/
│   └── fetch_rss.py             # RSS 수집 + 태깅 스크립트
├── .github/
│   └── workflows/
│       └── fetch.yml            # GitHub Actions 자동화
└── public/
    ├── index.html               # 웹앱 (여기서 열람)
    └── articles.json            # 수집된 아티클 (자동 생성)
```
