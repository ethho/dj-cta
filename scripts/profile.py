import time
from requests import get


def main():
    r = (
        100,
        600
    )
    for i in range(10, 1000, 10):
        if r[0] < i < r[1]:
            continue
        start = time.time()
        resp = get('http://localhost:8080', params={
            'duration': str(i)
        })
        print(f"{i=}, seconds={(time.time() - start):2f}")


if __name__ == '__main__':
    main()