<?
include "header.php";
include "config.php";    //데이터베이스 연결 설정파일
include "util.php";      //유틸 함수

$conn = dbconnect($host, $dbid, $dbpass, $dbname);

if (array_key_exists("player_id", $_GET)) {
    $player_id = $_GET["player_id"];
    $query = "select * from player natural join evaluation natural join team where player_id = $player_id";
    $res = mysqli_query($conn, $query);
    $player = mysqli_fetch_assoc($res);
    if (!$player) {
        msg("해당 선수가 존재하지 않습니다.");
    }
}
?>
    <div class="container fullwidth">

        <h3>선수 정보 상세 보기</h3>

        <p>
            <label for="player_id">선수 번호</label>
            <input readonly type="text" id="player_id" name="player_id" value="<?= $player['player_id'] ?>"/>
        </p>

        <p>
            <label for="player_name">선수 이름</label>
            <input readonly type="text" id="player_name" name="player_name" value="<?= $player['player_name'] ?>"/>
        </p>

        <p>
            <label for="nationality">국 적</label>
            <input readonly type="text" id="nationality" name="nationality" value="<?= $player['nationality'] ?>"/>
        </p>
        
        <p>
            <label for="age">나 이</label>
            <input readonly type="text" id="age" name="age" value="<?= $player['age'] ?>"/>
        </p>

        <p>
            <label for="team_name">소속 구단</label>
            <input readonly type="text" id="team_name" name="team_name" value="<?= $player['team_name'] ?>"/>
        </p>
        
        <p>
            <label for="strong_foot">주 발</label>
            <input readonly type="text" id="strong_foot" name="strong_foot" value="<?= $player['strong_foot'] ?>"/>
        </p>
        
        <p>
            <label for="price">시장가치</label>
            <input readonly type="text" id="price" name="price" value="<?= $player['price'] ?>"/>
        </p>
        
        <p>
            <label for="rating">평점</label>
            <input readonly type="text" id="rating" name="rating" value="<?= $player['rating'] ?>"/>
        </p>
        
        <p>
            <label for="comment_rating">현재 활약</label>
            <input readonly type="text" id="comment_rating" name="comment_rating" value="<?= $player['comment_rating'] ?>"/>
        </p>
        
        

    </div>
<? include("footer.php") ?>