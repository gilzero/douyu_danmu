from settings import Settings
from fetcher import Fetcher

if __name__ == '__main__':
    room_id = str(input("Please enter room ID (e.g 92000): "))
    print(f"📺 Room: {room_id}")

    max_results = int(input("Please enter maximum danmus you want to fetch (e.g 100): "))
    print(f"🔢 Maximum: {max_results}")

    settings = Settings(room_id=room_id, max_results=max_results)
    fetcher = Fetcher(settings)

    fetcher.run_fetch()

    fetcher.driver.quit()

    print(len(fetcher.danmus))

    fetcher.export_to_csv()
    print("Driver Closed. Bye")