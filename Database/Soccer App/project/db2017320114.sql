drop table product;
drop table manufacturer;


create table manufacturer(manufacturer_id int(11) not null auto_increment,
                            manufacturer_name varchar(255) not null, 
                            primary key(manufacturer_id));


create table product(product_id int(11) not null auto_increment,
                    manufacturer_id int(11) not null, 
                    product_name varchar(255) not null, 
                    product_desc text not null,
                    added_datetime datetime not null, 
                    price int(11) not null,
                    primary key(product_id), 
                    foreign key(manufacturer_id) references manufacturer(manufacturer_id));


insert into manufacturer values('111', 'Apple');
insert into manufacturer values('222', 'Samsung');
insert into manufacturer values('333', 'LG');

drop table player;
drop table team;
drop table evaluation;
drop table league;
drop table stadium;




create table stadium(
    stadium_id int not null auto_increment,
    stadium_name varchar(50) not null,
    constructed_year varchar(4) not null,
    capacity int(6) not null,
    place varchar(30) not null,
    primary key(stadium_id)
);

insert into stadium values(default, 'Tottenham Hotspur Stadium', '2016', 62850, 'London');
insert into stadium values(default, 'Old Trafford', '1909', 74140, 'Manchester');
insert into stadium values(default, 'Camp Nou', '1957', 99354, 'Barcelona');
insert into stadium values(default, 'Allianz Arena', '2002', 75024, 'Munchen');
insert into stadium values(default, 'Parc des Princes', '1972', 47929, 'Paris');




create table league(
    league_name varchar(30) not null,
    country varchar(20) not null,
    primary key(league_name)
);

insert into league values('English Premier League', 'England');
insert into league values('LaLiga', 'Spain');
insert into league values('Lega Serie A', 'Italy');
insert into league values('Ligue 1', 'France');
insert into league values('Bundesliga', 'Germany');
insert into league values('Liga Portugal', 'Portugal');

create table evaluation(
    rating int(3) not null,
    comment_rating varchar(20) not null,
    primary key(rating)
);
insert into evaluation values(1, '최악');
insert into evaluation values(2, '부진');
insert into evaluation values(3, '보통');
insert into evaluation values(4, '좋음');
insert into evaluation values(5, '아주 좋음');

create table team(
    team_id int not null auto_increment,
    team_name varchar(50) not null,
    manager varchar(20) not null,
    president varchar(20) not null,
    found_date date not null,
    league_name varchar(30) not null,
    stadium_id int not null,
    primary key(team_id),
    foreign key(stadium_id) references stadium(stadium_id) on delete cascade,
    foreign key(league_name) references league(league_name)
);

insert into team values(default, 'Tottenham Hotspur F.C.', 'Antonio Conte', 'Daniel Levy  ', '1882-09-05', 'English Premier League', '1');
insert into team values(default, 'Manchester United F.C.', 'Ole Gunnar Solskjaer', 'Glazer Family', '1878-03-05', 'English Premier League', '2');
insert into team values(default, 'F.C. Barcelona', 'Xavi Hernandez', 'Joan Laporta', '1899-11-29', 'LaLiga', '3');
insert into team values(default, 'FC Bayern Munchen', 'Julian Nagelsmann', 'Herbert Hainer', '1900-02-27', 'Bundesliga', '4');
insert into team values(default, 'Paris Saint-Germain F.C.', 'Mauricio Pochettino', 'Nasser Al-Khelaifi', '1970-08-12', 'Ligue 1', '5');


create table player(
    player_id int not null auto_increment,
    player_name varchar(30) not null,
    nationality varchar(20) not null,
    age int(3) not null,
    team_id int not null,
    strong_foot varchar(5) not null,
    rating int(3) not null,
    price varchar(30) not null,
    primary key(player_id),
    foreign key(team_id) references team(team_id) on delete cascade,
    foreign key(rating) references evaluation(rating)
);

insert into player values(default, 'Hugo Lloris', 'France', 34, '1', 'L', 4, '€9.00m');
insert into player values(default, 'Lionel Messi', 'Argentina', 34, '5', 'L', 4, '€100.00m');
insert into player values(default, 'Sergio Reguilon', 'Spain', 34, '1', 'L', 3, '€25.00m');
insert into player values(default, 'Jadon Sancho', 'England', 21, '2', 'R', 3, '€100.00m');
insert into player values(default, 'Pierre-Emile Höjbjerg', 'Denmark', 26, '1', 'R', 4, '€40.00m');
insert into player values(default, 'Joshua Kimmich', 'Germany', 26, '4', 'R', 4, '€90.00m');
insert into player values(default, 'Heung-min Son', 'South Korea', 29, '1', 'R', 5, '€85.00m');
insert into player values(default, 'Harry Winks', 'England', 25, '1', 'R', 3, '€20.00m');
insert into player values(default, 'Frenkie de Jong', 'Netherland', 24, '3', 'L', 4, '€90.00m');
insert into player values(default, 'Harry Kane', 'England', 28, '1', 'R', 3, '€120.00m');

