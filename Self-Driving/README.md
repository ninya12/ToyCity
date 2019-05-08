# README

Folder for self-driving code

## < Raspberry Pi >
 
### -- 차선 검출 --
>1. 카메라를 통해서 차선 검출
>2. 픽셀 중앙에서 소실점 까지 각도 계산
>3. 각도가 90도가 되도록 조향장치 조정

### -- 전 후진 --
> 1. 상태 확인
> - Parking인 경우 주차
>   - Parking
> - Drive인 경우 전진
>   - 장애물이 있는지 확인
>     - 장애물이 존재할 시 장애물이 사라질 때 까지 정지
>     - 장애물이 없으면 전진
 
 
### -- 조향 --
> 1. 상태 확인
> 2. 회전상태인 경우 회전.
 
### -- Localization --
> 1. 최초 위치 확인
> 2. 이동 시 scale에 맞도록 localization
> 3. 현 위치 송신
 
 
## < PC >
  
### -- 경로 --
> 1. 현재 위치 확인
> 2. 목적지 확인
> 3. 경로 탐색을 통해 command set 생성
> 4. command set 송신
