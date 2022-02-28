<?
include "header.php";
include "config.php";    //데이터베이스 연결 설정파일
include "util.php";      //유틸 함수

$conn = dbconnect($host, $dbid, $dbpass, $dbname);
$mode = "입력";
$action = "player_insert.php";

if (array_key_exists("player_id", $_GET)) { //수정 모드
    $player_id = $_GET["player_id"];
    $query =  "select * from player where player_id = $player_id";
    $res = mysqli_query($conn, $query);
    $player = mysqli_fetch_array($res);
    if(!$player) {
        msg("선수가 존재하지 않습니다."); //수정 누르기 전에 관리자가 삭제한게 아니라면 이 경우는 거의 존재하지 않음
    }
    $mode = "수정";
    $action = "player_modify.php";
    
    //echo json_encode($player);
}

$team = array();
$query = "select * from team";
$res = mysqli_query($conn, $query);
while($row = mysqli_fetch_array($res)) {
    $team[$row['team_id']] = $row['team_name'];
}

//$manufacturers[6] = 'OJW';
//echo json_encode($manufacturers);

?>
    <div class="container">
        <form name="player_register" action="<?=$action?>" method="post" class="fullwidth">
            <input type="hidden" name="player_id" value="<?=$player['player_id']?>"/>
            <h3>선수 정보 <?=$mode?></h3>
            <p>
                <label for="player_name">선수 이름</label>
                <input type="text" placeholder="이름 입력" id='player_name' name="player_name" value="<?=$player['player_name']?>"/>
            </p>

            <p>
                <label for="nationality">국 적</label>
                <input type="text" placeholder="국적 입력" id='nationality' name="nationality" value="<?=$player['nationality']?>" />
            </p>
            
            <p>
                <label for="age">나 이</label>
                <input type="text" placeholder="국적 입력" id='age' name="age" value="<?=$player['age']?>" />
            </p>
            
            <p>
                <label for="team_id">소속 구단</label>
                <select name="team_id" id="team_id">
                    <option value="-1">선택해 주십시오.(해당 구단 없을 시 구단 등록 필요)</option>
                    <?
                        foreach($team as $id => $name) {
                            if($id == $player['team_id']){
                                echo "<option value='{$id}' selected>{$name}</option>";
                            } else {
                                echo "<option value='{$id}'>{$name}</option>";
                            }
                        }
                    ?>
                </select>
            </p>
            
            <p>
                <label for="strong_foot">주 발</label>
                <input type="text" placeholder="주발 입력" id='strong_foot' name="strong_foot" value="<?=$player['strong_foot']?>" />
            </p>
            
            <p>
            	<label for='rating'>현재 평점</label>
            	<input type='text' placeholder='1(최악) 2(부진) 3(보통) 4(좋음) 5(아주 좋음)' id='rating' name='rating' value="<?=$player['rating']?>"/>
            </p>
            
            <p>
                <label for="price">시장가치</label>
                <input type="text" placeholder="시장가치(트랜스퍼마켓 유로 기준)" id='price' name="price" value="<?=$player['price']?>" />
            </p>
            

            <p align="center"><button class="button primary large" onclick="javascript:return validate();"><?=$mode?></button></p>

            <script>
                function validate() {
                    if(document.getElementById("team_id").value == "-1") {
                        alert ("소속 구단을 선택해 주십시오"); return false;
                    }
                    else if(document.getElementById("player_name").value == "") {
                        alert ("선수 이름을 입력해 주십시오"); return false;
                    }
                    else if(document.getElementById("nationality").value == "") {
                        alert ("국적을 입력해 주십시오"); return false;
                    }
                    else if(document.getElementById("age").value == "") {
                        alert ("나이를 입력해 주십시오"); return false;
                    }
                    else if(document.getElementById("strong_foot").value == "") {
                    	alert("주발을 입력해 주십시오"); return false;
                    }
                    else if(document.getElementById("rating").value == "") {
                        alert ("평점을 입력해 주십시오"); return false;
                    }
                    else if(document.getElementById("price").value == "") {
                        alert ("시장 가치를 입력해 주십시오"); return false;
                    }
                    return true;
                }
            </script>

        </form>
    </div>
<? include("footer.php") ?>