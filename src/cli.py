import os
import keyboard
import time

import ChatParser

from rich.progress import Progress, BarColumn
from rich.table import Table
from rich.console import Console


"""
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣶⣶⣄⠀⣀⣴⣦⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀ 
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣾⠟⠻⣿⣧⡀⠀⠀⠀⠀⠀⢀⣼⣿⠏⢀⣿⣴⣿⠟⠁⢹⡆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀ 
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣼⡏⠀⠀⣿⣿⡇⠀⠀⠀⠀⠀⣸⣿⡟⠀⣾⣷⣿⡟⠀⢀⡿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⡇⠀⣰⣿⡿⠀⠀⠀⠀⠀⢠⣿⣿⠃⣾⢟⣿⣿⠀⢀⣾⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣇⣴⣿⠟⠀⠀⠀⣀⣀⡀⢸⣿⣟⣼⠏⣸⣿⡇⢀⣾⠃⠀⠀⠀⣠⣤⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣿⡿⠛⣡⣷⣶⠀⣼⡟⢹⡗⢸⣿⣿⠏⠀⣿⣿⢀⡾⠁⠀⢀⣀⠀⣿⡍⢻⠀⠀⠀⠀⠀⢀⣀⣀⣀⣀⠀⠀⠀⠀⠀
⠸⣷⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣴⠟⣿⡇⢰⡟⢸⣿⢷⣿⠁⣾⠃⢸⣿⡏⠀⢰⣿⣿⡿⠁⠀⢰⣿⡿⠀⠈⠻⣿⠶⠶⠶⠟⠛⠋⠉⠉⠙⠛⢿⣶⣄⠀⠀
⠀⠈⠻⣦⣀⠀⠀⠀⠀⠀⠀⢀⣠⣴⠿⠋⠁⠀⣿⣷⣿⠁⢸⣿⠘⣿⣿⠃⣠⣾⣿⡇⠀⢸⣿⡟⠀⠀⢀⣾⣿⠇⠀⠀⢀⡿⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠻⣷⡀
⠀⠀⠀⠈⠉⠛⠿⠶⠶⠶⠿⠛⠉⠀⠀⠀⠀⠀⢸⣿⡇⠀⣸⣿⠀⣽⠿⠿⠛⠉⢿⣷⣶⠿⣿⣿⣄⣴⡾⠛⣿⣧⣀⣠⡟⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢻⣧
⠀⠀⠀⠀⠀⠀⠀⠀ ⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⡇⠀⢻⣿⣾⠋⠀⠀⠀⠀⠀⠉⠁⠀⠉⠛⠋⠉⠀⠀⠈⠉⠛⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠛⠃⠀⠈⠉⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠛
"""

console = Console()


def ResultView() :
    console.clear()
    table = Table(title="[bold][대화 내용 분석 결과][/bold]",title_justify="center")

    table.add_column("항목", justify="center", style="cyan", no_wrap=True)
    table.add_column("점수", style="magenta")
    # table.add_column("Box Office", justify="right", style="green")

    table.add_row("답장 시간", "평균 10분")
    table.add_row("", "")
    table.add_row("호감도", "90%")
    table.add_row("", "")
    table.add_row("", "")
    table.add_row("총평", "화이팅하세요!")

    console.print(table,justify="center")
    console.print("\n\n")
    console.print("메인 화면으로 돌아가려면 Enter키를 입력하세요.")
    while True :
        # test=1
        if keyboard.is_pressed('enter'): #엔터 키 입력
                time.sleep(0.1)
                break



def AnalyzeView(path) :
    
    with Progress() as progress:

        task1 = progress.add_task(f"[red]{path} 파일 분석중...", total=100)
        while not progress.finished:
            progress.update(task1, advance=0.5)
            time.sleep(0.02)

    try :
        result = ChatParser.ChatParser.parseOneFile(path)
        print(result)

    except Exception :
        console.print("[red bold]입력하신 파일을 분석하는데 실패하였습니다.\n다른 파일을 선택해 주세요.\n3초 뒤에 메인 화면으로 이동합니다.",justify="center")
        time.sleep(3.0)
        return -1

    return 1




def find_file(path:str) :
    
    file_list = os.listdir(path)
    file_list_txt = [file for file in file_list if file.endswith(".txt")]

    # console.print(file_list_txt)

    return file_list_txt

def MainView(index, file_list) :
    

    # os.system('clear')
    console.clear()
    console.print(
        """┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓\n"""
        """\n"""
        # """╔┓┏╦━━╦┓╔┓╔━━╗\n"""
        # """║┗┛║┗━╣┃║┃║╯╰║\n"""
        # """║┏┓║┏━╣┗╣┗╣╰╯║\n"""
        # """╚┛┗╩━━╩━╩━╩━━╝\n"""
"""[bold yellow]"""
"""
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣠⠤⠖⠒⠓⠑⠒⠢⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣴⠾⢋⣡⠖⠋⠉⠉⠉⠓⣦⣹⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣼⡿⢁⡾⠋⠀⠀⠀⠀⠀⠀⠀⢘⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣾⡟⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣰⣿⢋⣴⠏⠀⠀⠀⠀⠀⠀⠀⠀⡠⢾⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣿⡟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⣸⣿⠃⣼⠇⠀⠀⠀⠀⠀⠀⠀⠐⠚⠁⣾⡿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣿⠏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⢀⣿⡏⠠⣿⠀⠀⢀⠀⠀⠀⠀⠀⠀⢀⣾⡿⢁⣾⡟⠁⢠⣿⡟⠀⠀⡤⢪⣷⣀⣶⠟⠀⠀⠀⠀⠀⣰⣿⡯⠊⣹⡦⠀⠀⢀⣠⡶⠊⠙⡆⠀⢠⣾⡟⠀⢠⣿⠏⠀⢀⡔⢪⣷⢠⣶⠟⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⣿⡃⠀⢻⡄⠸⣿⡇⠀⠀⠀⠀⣠⣿⠟⢠⣿⡟⠀⣠⣿⠏⠀⣠⠞⢠⣿⣯⡏⠁⢠⠄⠀⠀⠀⣰⣿⠟⠀⣴⣿⠋⢀⣴⣿⠋⠀⣴⡿⠃⢠⣿⠏⠀⣰⣿⠏⠀⣠⠋⣠⣿⣿⠋⠀⣠⠄⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠹⣇⠀⠀⠈⠉⠁⠀⠀⢀⣴⠾⠋⠁⢠⣿⠏⠀⣴⣿⠏⢀⡴⠁⣠⣿⠏⠈⠓⠒⠁⠀⠀⠀⣼⣿⠃⠀⣾⡿⠃⣠⢾⣿⠃⠀⢀⡝⠕⢺⣿⠏⢀⣼⣿⠋⢀⡜⠁⣰⣿⠏⠈⠓⠚⠁⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⠳⢤⣀⣀⣠⠤⠖⠋⠁⠀⠀⠀⠀⠻⠦⠋⠈⠻⠔⠊⠀⠰⠿⠋⠀⠀⠀⠀⠀⠀⠀⠼⠻⠁⠀⠀⠙⠧⠒⠁⠀⠙⠦⠒⠋⠀⠀⠈⠻⠔⠊⠈⠻⠔⠋⠀⠼⠻⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
"""
"""[/bold yellow]"""
        """\n"""
        """\n"""     
        """이 프로그램은 카카오톡 대화를 분석하는 프로그램 입니다.\n"""
        """원하는 상대와의 대화를 분석하여 상대의 호감도를 알고 싶다면\n"""
        """프로그램과 같은 폴더에 확장자가 "txt"인 카카오톡 대화 파일을 넣어 주세요!! \n"""
        """[cyan italic]내보내기 방법 : 카카오톡 > 채팅방 설정 > 대화 내용 관리 > 대화 내용 저장\n[/cyan italic]"""
        """\n"""
        """┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛\n"""
        ,justify="center")
    
    console.print("[italic cyan] [bold]파일 선택[/bold] (상하 방향키로 조작하고, 엔터를 눌러 선택하세요)  [/italic cyan]", justify="center")
    for i in range(len(file_list)) :
        if i == index : console.print(f"   > {file_list[i]}", style="bold red")
        else : console.print("     "+file_list[i], style="dim")



def InitialFunction() :
    breakFlag = False
    selectIdx = 0
    findDirectory = "./"
    file_list_txt = find_file(findDirectory)

    while True : 
        if breakFlag == True : 
            break

        MainView(selectIdx, file_list=file_list_txt)
        while True :
            if keyboard.is_pressed(80): #아래쪽 방향키 입력
                
                time.sleep(0.2)

                if(selectIdx < len(file_list_txt)-1) :
                    selectIdx+=1
                    break

            if keyboard.is_pressed(72): #위쪽 방향키 입력
                
                time.sleep(0.2)
                if(selectIdx > 0) :
                    selectIdx-=1
                    break

            if keyboard.is_pressed('enter'): #엔터 키 입력
                time.sleep(0.2)
                ret = AnalyzeView(f"{findDirectory}{file_list_txt[selectIdx]}")
                if ret == -1 :
                    break

                ResultView()
                break


if __name__ == "__main__":
    InitialFunction()

