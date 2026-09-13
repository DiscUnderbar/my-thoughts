# Tennin 언어 명세 (v0.1)

Tennin은 소스 코드를 독립적인 `.tennbc` 바이트코드로 컴파일하고, 스택 기반 가상 머신(VM)이 이를 실행하는 언어다. 인터프리터가 소스 텍스트를 직접 평가하지 않는다.

## 실행 모델

`tenn program.tenn`은 lex/parse/compile을 거쳐 메모리의 bytecode를 VM으로 보낸다.

```powershell
tenn program.tenn                    # 소스 컴파일 후 실행
tenn program.tenn -o program.tennbc  # 바이트코드 파일 생성
tenn program.tennbc                  # 바이트코드 실행
```

`.tennbc`는 `TENN\x01` 헤더를 가진 이진 파일이다. `--pack`은 VM 실행 파일 뒤에 bytecode를 붙인 실행 가능한 `.tenn` 파일을 생성한다.

## 문법

```tennin
// 변수 선언과 대입. 문장은 ; 로 끝난다.
let count = 3;
count = count - 1;

// 값 출력
print "remaining: " + count;

// 조건문. else는 선택 사항이다.
if (count == 0) {
  print "done";
} else {
  print "working";
}

// 반복문과 블록
while (count > 0) {
  print count;
  count = count - 1;
}

// 사용할 수 있는 값과 연산자
let integer = 42;
let text = "hello";
let flag = true;
let result = !(integer <= 10);
```

지원하는 연산자는 `+`, `-`, `*`, `/`, `-값`, `!값`, `==`, `!=`, `<`, `<=`, `>`, `>=`이다. 문자열에는 `+`만 쓸 수 있다.

## 의미

- 값은 64-bit 정수, 문자열, 불리언이다. 선언되지 않은 변수와 0으로 나누기는 실행 오류다.
- `+`는 정수 덧셈 또는 문자열 이어붙이기, 나머지 산술 연산은 정수에만 적용된다.
- 조건문에서 `false`, `0`, 빈 문자열만 거짓이다.
- 비교와 논리 부정은 불리언을 만든다. 블록은 범위를 새로 만들지 않는다.
- 문장은 세미콜론으로 끝나며, `if`, `while`, 블록은 예외다.
