# ammonia-supply-risk

공개 배포용으로 정리한 암모니아 공급설비 위험 선별 도구입니다.

이 저장소는 원 연구의 **재현 가능한 핵심 계산 예시**만 담습니다.
저작권·라이선스가 확인되지 않은 논문 원문, 상용 시뮬레이터 파일, 외부 코드, 원자료는 포함하지 않았습니다.

## 포함 내용

- `material_screening`: STS304, STS316L, STS317을 포함한 10개 재료의 조건부 손상 프록시 비교
- `conditional_risk`: 기준 빈도에 재료·용접·환경·검사 계수를 투명하게 곱하는 계산
- `mutually_exclusive_paths`: 하나의 시작사건 빈도를 배타적 보호경로에 한 번만 배분하는 계산
- `data/qualified_sobol_summary.csv`: 수렴 기준을 통과한 7개 출력의 요약표

재료 점수는 연간 누출빈도가 아닙니다. 실제 빈도 산출에는 재료별 사용시간, 고장건수, 균열성장 자료, 초기 결함분포, 파괴기준, 검사 검출확률(POD)이 필요합니다.

## 빠른 사용

```python
from ammonia_supply_risk import material_screening, conditional_risk

rows = material_screening(n_samples=10_000)
screening_index = conditional_risk(1.0e-4, material_factor=1.2)
```

## 연구·인용

저자: Ugwiyeon Lee, Seong-Yun Bae, Hakrae Kim, Jungsu Lee, Jinseo Kim  
소속: Gas Safety R&D Institute, Korea Gas Safety Corporation  
연락처: lyullee@kgs.or.kr

Funding: This work was supported by the Korea Institute of Energy Technology Evaluation and Planning (KETEP), funded by the Korea government (Ministry of Climate, Energy and Environment) [grant number RS-2024-00437207]. The funder had no role in study design, data collection, analysis or interpretation, manuscript preparation, or the decision to submit the article.

릴리스 DOI: https://doi.org/10.5281/zenodo.23550690
