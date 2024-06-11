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
from InsightsByPeriod import InsightsByPeriod

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


def ResultView(result: MessageHistory, personInfos: List[PersonInfo], myName: str) :
    console.clear()
    personInfoTble = Table(title="[bold][대화 내용 분석 결과][/bold]",title_justify="center")

    # myPersonInfo must be the first element
    myPersonInfo = None
    for p in personInfos:
        if p.name == myName:
            myPersonInfo = p
            break
    personInfos.remove(myPersonInfo)
    personInfos.insert(0, myPersonInfo)

    personInfoTble.add_column("항목", justify="center", style="cyan", no_wrap=True)
    for name in [p.name for p in personInfos]:
        personInfoTble.add_column(name, justify="center", style="magenta")
    # table.add_column("Box Office", justify="right", style="green")

    values = {}
    for p in personInfos:
        d = p.asDict()
        for k in d.keys():
            if k == "이름":
                continue

            if k not in values:
                values[k] = []
            value = d[k]
            if type(value) == float:
                values[k].append(f"{value:.2f}")
            else:
                values[k].append(str(value))

    for k in values.keys():
        personInfoTble.add_row(k, *values[k])


    # Monthly Insights
    monthlyTable = Table(title="[bold][월별 분석][/bold]",title_justify="center")
    monthlyInsights = InsightsByPeriod.createMonthly(result)
    monthlyTable.add_column("기간", justify="center", style="cyan")
    monthlyTable.add_column("메세지 수", justify="center", style="magenta")
    for insight in monthlyInsights:
        monthlyTable.add_row(f"{insight.periodStart} ~ {insight.periodEnd}", str(len(insight.messages)))

    # Yearly Insights
    yearlyTable = Table(title="[bold][연도별 분석][/bold]",title_justify="center")
    yearlyInsights = InsightsByPeriod.createYearly(result)
    yearlyTable.add_column("기간", justify="center", style="cyan")
    yearlyTable.add_column("메세지 수", justify="center", style="magenta")
    for insight in yearlyInsights:
        yearlyTable.add_row(f"{insight.periodStart.year}", str(len(insight.messages)))

    # Yearly + Monthly Insights
    insightsByYear = {} # year -> [InsightsByPeriod]
    for insight in monthlyInsights:
        year = insight.periodStart.year
        if year not in insightsByYear:
            insightsByYear[year] = []
        insightsByYear[year].append(insight)

    # sort by month
    for year in sorted(insightsByYear.keys()):
        insightsByYear[year].sort(key=lambda x: x.periodStart.month)

    periodTable = Table(title="[bold][기간별 메세지 수 분석][/bold]",title_justify="center")
    periodTable.add_column("연도", justify="center", style="cyan")
    for month in range(1, 13):
        periodTable.add_column(str(month) +"월", justify="center", style="cyan")

    for year in sorted(insightsByYear.keys()):
        row = [str(year)]
        for month in range(1, 13):
            found = False
            for insight in insightsByYear[year]:
                if insight.periodStart.month == month:
                    row.append(str(len(insight.messages)))
                    found = True
                    break
            if not found:
                row.append("0")
        periodTable.add_row(*row)


    console.print(personInfoTble, justify="center")
    #console.print(monthlyTable, justify="center")
    #console.print(yearlyTable, justify="center")
    console.print(periodTable, justify="center")

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
            # test : 영상 제작용 가짜 이름으로 대체
            uiState.name_list = ["겐지", uiState.file_list[uiState.selectedFileIdx].split('.')[0]]
            #uiState.name_list = list(messageHistory.messagesBySender.keys())

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
            personInfos = createPersonInfos(messageHistory)
            # test: 영상 제작용 가짜 이름으로 대체
            personInfos[0].name = myName
            personInfos[1].name = uiState.file_list[uiState.selectedFileIdx].split('.')[0]
            #
            ResultView(messageHistory, personInfos, myName)
            uiState.Reset()
            break


if __name__ == "__main__":
    InitialFunction()

