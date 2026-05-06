# 경쟁사 로고 (v6 비교 그리드용)

v6 사전 등록 페이지의 경쟁사 비교 섹션(`#vs`)에서 각 컬럼 상단에 표시되는 앱 로고.

## 현재 사용 중인 로고 소스

**실제 Google Play Store CDN 아이콘을 직접 참조** (`play-lh.googleusercontent.com`). 정확한 공식 아이콘을 표시하기 위해.

| 앱 | Play Store 패키지 | 아이콘 URL 포맷 |
|---|---|---|
| Character.AI | `ai.character.app` | `play-lh.googleusercontent.com/dAVjIN_4fD...=w240-h480` |
| Replika | `ai.replika.app` | `play-lh.googleusercontent.com/UGRlMthHHNvFrbk...=w240-h480` |
| Talkie | `com.weaver.app.prod` | `play-lh.googleusercontent.com/tKZupmt2DEsC...=w240-h480` |
| Chai | `com.Beauchamp.Messenger.external` | `play-lh.googleusercontent.com/4MERnA5CP1fHDL16ZJ...=w240-h480` |
| 크랙 (Crack) | `com.wrtn.character` | `play-lh.googleusercontent.com/FZyGa-a0Yct-SGk64tQBjC...=w240-h480` |
| 제타 (zeta) | `com.scatterlab.messenger` | `play-lh.googleusercontent.com/7BHCCDafgblr3UBNNx-ELJ...=w240-h480` |

## 폴백 SVG (백업용)

초기 개발용으로 만든 SVG 재현본은 유지 (CDN 장애 시 빠른 교체 가능):
- [character-ai.svg](character-ai.svg) / [replika.svg](replika.svg) / [talkie.svg](talkie.svg)
- [chai.svg](chai.svg) / [crack.svg](crack.svg) / [zeta.svg](zeta.svg)
- [lucive.svg](lucive.svg) — 자사 로고

팀에서 정식 브랜드 에셋(공식 프레스 킷 SVG)을 확보하면 이 파일명으로 덮어쓰고 HTML의 `<img src>`를 로컬 경로로 바꾸면 됩니다.

## 법적 근거 및 주의 사항

### 현재 랜딩 페이지 컨텍스트
경쟁사 아이콘을 비교 마케팅 목적으로 사용하는 것은 **nominative fair use** (지칭적 공정 사용) 원칙 하에 다음 조건 충족 시 일반적으로 허용:
1. 해당 제품을 식별하는 데 필요한 최소 범위만 사용
2. **후원·제휴·승인 관계 암시 없음**
3. 사실에 기반한 비교 (→ 모든 인용은 실제 Google Play 리뷰 원문)
4. 상표권자 이미지를 **변형하지 않고** 원본 그대로 사용 (→ Play Store CDN 직접 참조)

### 안정성 이슈
Play Store CDN URL은 **이론적으로 변경될 수 있음**:
- 각 이미지 ID는 Google이 관리 (드물지만 앱 업데이트 시 아이콘 URL 재발급 가능)
- Hotlinking 차단 정책 변화 가능성 (현재는 무제한 허용)

**정식 런칭 전** 권장 작업:
1. Play Store CDN에서 이미지 파일 다운로드
2. `pre-register/assets/logos/` 하위에 저장 (예: `character-ai-playstore.png`)
3. HTML의 `<img src>`를 로컬 경로로 교체

### 사용 범위 주의
- ✅ **랜딩 페이지**: 일반적으로 가장 안전한 컨텍스트
- ⚠️ **Play Store / App Store 리스팅**: comparative marketing 정책 확인 필요
- ⚠️ **유료 광고 소재** (X Ads, 네이버, Google Ads): 각 플랫폼별 타 브랜드 표시 가이드라인 준수 필요

## 로고 교체 가이드

### 방법 1: 정식 브랜드 에셋으로
1. 각 회사의 press/brand kit에서 공식 SVG/PNG 다운로드
2. 이 폴더에 파일명 맞춰 저장
3. HTML의 `<img src="https://play-lh.googleusercontent.com/...">`를 `<img src="assets/logos/character-ai.svg">`로 변경

### 방법 2: Play Store 이미지 로컬 캐싱 (권장)
1. 현재 참조 중인 Play Store URL에서 이미지 다운로드 (wget/curl)
2. 128px 또는 256px로 리사이즈 (wand 또는 ImageMagick)
3. 로컬 경로로 `<img src>` 변경

## 참고 링크
- [Character.AI on Play Store](https://play.google.com/store/apps/details?id=ai.character.app)
- [Replika on Play Store](https://play.google.com/store/apps/details?id=ai.replika.app)
- [Talkie on Play Store](https://play.google.com/store/apps/details?id=com.weaver.app.prod)
- [Chai on Play Store](https://play.google.com/store/apps/details?id=com.Beauchamp.Messenger.external)
- [크랙 on Play Store](https://play.google.com/store/apps/details?id=com.wrtn.character)
- [제타 on Play Store](https://play.google.com/store/apps/details?id=com.scatterlab.messenger)
