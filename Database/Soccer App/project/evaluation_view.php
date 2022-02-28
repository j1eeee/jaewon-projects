<?
include "header.php";
include "config.php";    //데이터베이스 연결 설정파일
include "util.php";      //유틸 함수

$conn = dbconnect($host, $dbid, $dbpass, $dbname);

if (array_key_exists("rating", $_GET)) {
    $rating = $_GET["rating"];
    $query = "select * from evaluation where rating = $rating";
    $res = mysqli_query($conn, $query);
    $evaluation = mysqli_fetch_assoc($res);
    if (!$evaluation) {
        msg("해당 구단이 존재하지 않습니다.");
    }
}
?>
    <div class="container fullwidth">

        <h3>평점 설명 보기</h3>

        <p>
            <label for="rating">평점</label>
            <input readonly type="text" id="rating" name="rating" value="<?= $evaluation['rating'] ?>"/>
        </p>

        <p>
            <label for="comment_rating">활약도</label>
            <input readonly type="text" id="comment_rating" name="comment_rating" value="<?= $evaluation['comment_rating'] ?>"/>
        </p>
    </div>
<? include("footer.php") ?>