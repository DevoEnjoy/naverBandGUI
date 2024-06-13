import datetime

class DateTimer:
    def get_current_datetime(self, format_str:str=None):
        """
        현재 날짜와 시간을 반환합니다. 
        format_str 인자를 통해 특정 형식으로 날짜와 시간을 반환할 수 있습니다.
        format_str 인자가 없다면 
        :param format_str: 날짜와 시간의 형식을 지정하는 문자열 (예: "yyyy-MM-dd HH:mm:ss")
            - "yyyy": 연도의 4자리
            - "yy": 연도의 마지막 두 자리
            - "MM": 월의 두 자리 (1월이라면 "01")
            - "dd": 일의 두 자리
            - "HH": 24시간 기준의 시간 두 자리
            - "hh": 12시간 기준의 시간 두 자리
            - "mm": 분의 두 자리
            - "ss": 초의 두 자리
        :return: 현재 날짜와 시간 (format_str에 따라 문자열 또는 datetime.datetime 객체)
        """
        current_datetime = datetime.datetime.now()

        if not format_str:
            return current_datetime

        # 주어진 형식에 따라 날짜와 시간을 변환합니다.
        format_str = format_str.replace("yyyy", "%Y")
        format_str = format_str.replace("yy", "%y")
        format_str = format_str.replace("MM", "%m")
        format_str = format_str.replace("dd", "%d")
        format_str = format_str.replace("HH", "%H")
        format_str = format_str.replace("hh", "%I")
        format_str = format_str.replace("mm", "%M")
        format_str = format_str.replace("ss", "%S")

        return current_datetime.strftime(format_str)

    def get_current_date(self):
        return self.get_current_datetime().date()

    def get_current_time(self):
        return self.get_current_datetime().time()

    def create_custom_datetime(self, year, month, day, hour, minute, second):
        return datetime.datetime(year, month, day, hour, minute, second)

    def create_custom_date(self, year, month, day):
        return datetime.date(year, month, day)

    def create_custom_time(self, hour, minute, second):
        return datetime.time(hour, minute, second)

if __name__ == "__main__":
    # 클래스의 인스턴스 생성
    datetime_utility = DateTimer()

    # 예제 메서드 호출
    print("현재 날짜와 시간:", datetime_utility.get_current_datetime())
    print("현재 날짜:", datetime_utility.get_current_date())
    print("현재 시간:", datetime_utility.get_current_time())

    custom_datetime = datetime_utility.create_custom_datetime(2023, 9, 27, 14, 30, 0)
    print("특정 날짜와 시간:", custom_datetime)

    custom_date = datetime_utility.create_custom_date(2023, 9, 27)
    print("특정 날짜:", custom_date)

    custom_time = datetime_utility.create_custom_time(14, 30, 0)
    print("특정 시간:", custom_time)