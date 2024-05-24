# Template Dag Repository for Vane Airflow
Vane Airflow를 생성할 때 사용할 Dag Repository Template

### 디렉토리 구조
- /dags : Dag 코드가 위치
- /plugins: Plugins 모듈 위치
- /tests: Dag Test 코드가 위치

### 테스트 수행 가이드
- Pycharm으로 실행시 Settings >> Project Structure 에서 dags, plugins 폴더를 Source Folder로 설정해주셔야합니다.
- pytest, pytest-mock 패키지가 설치되어 있어야 합니다.
- 로컬환경에서 테스트를 수행하기 전 코드에서 사용된 패키지들을 install 해주세요. vane Airflow 이미지에 있는 requirements.txt 파일을 저장소에 복사해 pip install을 하시면 편합니다.
  - requirements.txt 파일은 다음과 같이 다운로드 가능합니다.
  - aim 내 airflow 목록에서 해당 저장소와 연결된 Airflow를 클릭합니다.
    <img width="1530" alt="스크린샷 2023-07-11 오후 6 09 14" src="https://github.com/sktaiflow/dag-vane-template/assets/111335140/55c186e8-bb01-4ba0-827f-7aff135ec007">
  - Image 정보 안에 있는 패키지 목록을 클릭한 후 다운로드를 눌러 requirements.txt를 다운받습니다.
    <img width="1444" alt="스크린샷 2023-07-11 오후 6 11 52" src="https://github.com/sktaiflow/dag-vane-template/assets/111335140/5db891ac-f682-41ae-9ed3-1bcdbb9683c4">

- 테스트를 진행하지 않을 DAG의 경우 tests/.dagtestignore 파일에 DAG 파일명을 추가해주세요.
