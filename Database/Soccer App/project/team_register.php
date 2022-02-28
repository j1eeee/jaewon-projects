<?
include "header.php";
include "config.php";    //데이터베이스 연결 설정파일
include "util.php";      //유틸 함수

$conn = dbconnect($host, $dbid, $dbpass, $dbname);
$mode = "입력";
$action = "team_insert.php";

if (array_key_exists("team_id", $_GET)) { //수정 모드
    $team_id = $_GET["team_id"];
    $query =  "select * from team where team_id = $team_id";
    $res = mysqli_query($conn, $query);
    $team = mysqli_fetch_array($res);
    if(!$team) {
        msg("구단이 존재하지 않습니다."); //수정 누르기 전에 관리자가 삭제한게 아니라면 이 경우는 거의 존재하지 않음
    }
    $mode = "수정";
    $action = "team_modify.php";
    
}
$league = array();
$query_league = "select * from league";
$res_league = mysqli_query($conn, $query_league);
while($row_league = mysqli_fetch_array($res_league)) {
	$league[$row_league['league_name']] = $row_league['league_name'];
}

$stadium = array();
$query = "select * from stadium";
$res = mysqli_query($conn, $query);
while($row = mysqli_fetch_array($res)) {
    $stadium[$row['stadium_id']] = $row['stadium_name'];
}

?>
    <div class="container">
        <form name="team_register" action="<?=$action?>" method="post" class="fullwidth">
            <input type="hidden" name="team_id" value="<?=$team['team_id']?>"/>
            <h3>구단 정보 <?=$mode?></h3>
            <p>
                <label for="team_name">구단 이름</label>
                <input type="text" placeholder="이름 입력" id='team_name' name="team_name" value="<?=$team['team_name']?>"/>
            </p>

            <p>
                <label for="manager">감 독</label>
                <input type="text" placeholder="감독 입력" id='manager' name="manager" value="<?=$team['manager']?>" />
            </p>
            
            <p>
                <label for="president">회 장</label>
                <input type="text" placeholder="회장 입력" id="president" name="president" value="<?=$team['president']?>" />
            </p>

            <p>
                <label for="found_date">창 단</label>
                <input type="date" placeholder="창단 날짜 입력" id="found_date" name="found_date" value="<?=$team['found_date']?>" />
            </p>
            
            <p>
            	<label for="league_name">소속 리그</label>
            	<select name="league_name" id='league_name'>
            		<option value='-1'>선택해 주십시오</option>
            		<?
            			foreach($league as $id => $name) {
            				if($id == $team['league_name']){
            					echo "<option value = '{$id}' selected>{$name}</option>";
            				} else {
            					echo "<option value='{$id}'>{$name}</option>";
            				}
            			}
            		?>
            	</select>
            </p>
            
            <p>
                <label for="stadium_id">홈 구장</label>
                <select name="stadium_id" id="stadium_id">
                    <option value="-1">선택해 주십시오.(해당 구장 없을 시 구장 등록 필요)</option>
                    <?
                        foreach($stadium as $id => $name) {
                            if($id == $team['stadium_id']){
                                echo "<option value='{$id}' selected>{$name}</option>";
                            } else {
                                echo "<option value='{$id}'>{$name}</option>";
                            }
                        }
                    ?>
                </select>
            </p>
            

            <p align="center"><button class="button primary large" onclick="javascript:return validate();"><?=$mode?></button></p>

            <script>
                function validate() {
                    if(document.getElementById("stadium_id").value == "-1") {
                        alert ("홈 구장을 선택해 주십시오"); return false;
                    }
                    else if(document.getElementById("league_name").value == "-1") {
                    	alert ("소속 리그를 선택해 주십시오"); return false;
                    }
                    else if(document.getElementById("team_name").value == "") {
                        alert ("구단 명을 입력해 주십시오"); return false;
                    }
                    else if(document.getElementById("manager").value == "") {
                        alert ("감독을 입력해 주십시오"); return false;
                    }
                    else if(document.getElementById("president").value == "") {
                        alert ("회장을 입력해 주십시오"); return false;
                    }
                    else if(document.getElementById("rating").value == "") {
                        alert ("창단 날짜를 입력해 주십시오"); return false;
                    }
                    return true;
                }
            </script>

        </form>
    </div>
<? include("footer.php") ?>