from crewai import Task
from textwrap import dedent
from datetime import date

class BATasks():
  def summary_requirement_task(self, agent, file_path, callback):
    print(f"solution callback {callback}")
    return Task(
      description=dedent(
        f"""
        Đọc file `{file_path}` và tổng hợp các yêu cầu nghiệp vụ phục vụ thiết kế kiến trúc hệ thống.
        """),
        async_execution=False,
        agent=agent,
        expected_output="""
        Một đoạn văn bản mô tả yêu cầu nghiệp vụ rõ ràng, súc tích, sẵn sàng cho SA dùng.
        """,
        # output_file="solution.txt",
        callback=callback,
      )


