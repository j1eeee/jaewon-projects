<!DOCTYPE html>
<html lang="ko">
  <head>
    <title>축덕대학</title>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <link rel="stylesheet" href="styles.css" />
  </head>
  <body>
    <div class="navbar fixed">
      <div class="container">
        <a class="pull-left title" href="index.php">축덕대학</a>
        <ul class="pull-right">
          <li>
            <form action="player_list.php" method="post">
              <input
                type="text"
                name="search_keyword"
                placeholder="선수 통합검색"
              />
            </form>
          </li>

          <li>
            <form action="team_list.php" method="post">
              <input
                type="text"
                name="search_keyword"
                placeholder="구단 통합검색"
              />
            </form>
          </li>
          
          <li>
            <form action="stadium_list.php" method="post">
              <input
                type="text"
                name="search_keyword"
                placeholder="구장 통합검색"
              />
            </form>
          </li>
          
          <li><a href="player_list.php">선수 목록</a></li>
          <li><a href="team_list.php">팀 목록</a></li>
          <li><a href="stadium_list.php">구장 목록</a></li>
          <li><a href="site_info.php">소개</a></li>
        </ul>
      </div>
    </div>
  </body>
</html>