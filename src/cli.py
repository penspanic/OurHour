import os
import keyboard
import time

import ChatParser

from rich.progress import Progress, BarColumn
from rich.table import Table
from rich.console import Console

from MessageHistory import MessageHistory
from PersonInfo import PersonInfo
from Utils import *

class UIState:
    def __init__(self):
        self.uiStep = 0
        self.selectedFileIdx = 0
        self.selectedNameIdx = 0
        self.findDirectory = ''
        self.file_list = []
        self.name_list = []
        self.analyze_result_list = []
        
    def Reset(self):
        self.uiStep = 0
        self.selectedFileIdx = 0
        self.selectedNameIdx = 0
        self.findDirectory = ''
        #self.file_list = [] 계속 사용
        self.name_list = []
        self.analyze_result_list = []


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


def ResultView(result: MessageHistory, myPersonInfo: PersonInfo) :
    console.clear()
    table = Table(title="[bold][대화 내용 분석 결과][/bold]",title_justify="center")

    table.add_column("항목", justify="center", style="cyan", no_wrap=True)
    table.add_column("수치", style="magenta")
    # table.add_column("Box Office", justify="right", style="green")

    personInfos = createPersonInfos(result)
    myPersonInfo = personInfos
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



def AnalyzeView(path) -> MessageHistory:
    
    with Progress() as progress:

        task1 = progress.add_task(f"[red]{path} 파일 분석중...", total=100)
        while not progress.finished:
            progress.update(task1, advance=10)
            time.sleep(0.02)

    try :
        result = ChatParser.ChatParser.parseOneFile(path)

    except Exception :
        # for i in range(3,0,-1) :
        #     console.clear()
        #     console.print(f"[red bold]입력하신 파일을 분석하는데 실패하였습니다.\n다른 파일을 선택해 주세요.\n{i}초 뒤에 메인 화면으로 이동합니다.",justify="center")
        #     time.sleep(1)
        console.print(f"[red bold]입력하신 파일을 분석하는데 실패하였습니다.\n다른 파일을 선택해 주세요.\n3초 뒤에 메인 화면으로 이동합니다.",justify="center")
        time.sleep(3)
            
        return None

    return result


def find_file(path:str) :
    
    file_list = os.listdir(path)
    file_list_txt = [file for file in file_list if file.endswith(".txt")]

    # console.print(file_list_txt)

    return file_list_txt

def MainView(uiState: UIState) :
    

    # os.system('clear')
    console.clear()
    console.print(
        """┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓\n"""
        # """\n"""
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
        """[magenta]프로그램을 종료하려면 ESC키를 눌러주세요.\n[/magenta]"""
        """[cyan italic]내보내기 방법 : 카카오톡 > 채팅방 설정 > 대화 내용 관리 > 대화 내용 저장\n[/cyan italic]"""
        """\n"""
        """┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛\n"""
        ,justify="center")
    
    if uiState.uiStep == 0:
        console.print("[italic cyan] [bold]파일 선택[/bold] (상하 방향키로 조작하고, 엔터를 눌러 선택하세요)  [/italic cyan]", justify="center")
        for i in range(len(uiState.file_list)) :
            if i == uiState.selectedFileIdx : console.print(f"   > {uiState.file_list[i]}", style="bold red")
            else : console.print("     "+uiState.file_list[i], style="dim")
    elif uiState.uiStep == 1:
        console.print("[italic cyan] 내 이름을 고르세요  [/italic cyan]", justify="center")
        for i in range(len(uiState.name_list)) :
            if i == uiState.selectedNameIdx : console.print(f"   > {uiState.name_list[i]}", style="bold red")
            else : console.print("     "+uiState.name_list[i], style="dim")


selectedFileIdx = 0
selectedNameIdx = 0


def InitialFunction() :
    breakFlag = False
    uiState = UIState()
    uiState.findDirectory = "./"
    uiState.file_list = find_file(uiState.findDirectory)
    while True : 
        if breakFlag == True : 
            break

        MainView(uiState)
        if uiState.uiStep == 0:
            FileSelect(uiState)
        elif uiState.uiStep == 1:
            if len(uiState.analyze_result_list) > 0:
                NameSelect(uiState.analyze_result_list[0], uiState)


def FileSelect(uiState: UIState) :

    while True :
        if keyboard.is_pressed(80): #아래쪽 방향키 입력
            
            time.sleep(0.2)

            if(uiState.selectedFileIdx < len(uiState.file_list)-1) :
                uiState.selectedFileIdx+=1
                break

        if keyboard.is_pressed(72): #위쪽 방향키 입력
            
            time.sleep(0.2)
            if(uiState.selectedFileIdx > 0) :
                uiState.selectedFileIdx-=1
                break

        if keyboard.is_pressed('enter'): #엔터 키 입력
            time.sleep(0.2)
            messageHistory = AnalyzeView(f"{uiState.findDirectory}{uiState.file_list[uiState.selectedFileIdx]}")
            if messageHistory is None:
                break

            uiState.analyze_result_list.append(messageHistory)
            uiState.name_list = list(messageHistory.messagesBySender.keys())

            uiState.uiStep = 1
            #ResultView(messageHistory)
            break
        if keyboard.is_pressed('ESC'): #ESC 키 입력
            breakFlag=True  
            break

def NameSelect(messageHistory: MessageHistory, uiState: UIState):
    while True :
        if keyboard.is_pressed(80): #아래쪽 방향키 입력    
            time.sleep(0.2)
            if(uiState.selectedNameIdx < len(uiState.name_list)-1) :
                uiState.selectedNameIdx+=1
                break

        if keyboard.is_pressed(72): #위쪽 방향키 입력
            
            time.sleep(0.2)
            if(uiState.selectedNameIdx > 0) :
                uiState.selectedNameIdx-=1
                break

        if keyboard.is_pressed('enter'): #엔터 키 입력
            time.sleep(0.2)
            myName = uiState.name_list[uiState.selectedNameIdx]
            myPersonInfo = createPersonInfo(messageHistory, myName)
            ResultView(messageHistory, myPersonInfo)
            uiState.Reset()
            break


if __name__ == "__main__":
    InitialFunction()

