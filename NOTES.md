# 십자 셈놀이 (가족용 크로스매스)
- 단일 파일 index.html, 광고/결제 없음, 진행·통계는 브라우저 localStorage
- 모드: 난이도 4단계(레벨 시드 고정), 오늘의 문제(날짜 시드), 무한 도전(제출 시 채점, 연속 성공 시 난이도 상승)
- 생성기: 십자 배치 + 한 식씩 풀리는지 전파 검증(800개 테스트 통과)
- PWA: `python3 build.py` → docs/ (index.html + manifest + sw.js + 아이콘). 원본은 루트 index.html(아티팩트용). 레벨은 시드로 기기에서 생성 → 데이터 없이 전 레벨 오프라인. 폰트는 앱 사용 글자만 서브셋해서 SW 설치 때 미리 캐시
- 배포: GitHub qpwo5470/sem-cross, Pages(main /docs) → https://qpwo5470.github.io/sem-cross/ (맥 ~/Projects/sem-cross 에서 push)
