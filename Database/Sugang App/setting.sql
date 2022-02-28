drop table my_result;
drop table course;
drop table professor;
drop table department;
drop table info;

create table info(id varchar(20), pw varchar(20) not null, primary key(id));
create table department(dept_name varchar(20), college varchar(20), primary key(dept_name));
create table professor(prof_name varchar(20), dept_name varchar(20) references department(dept_name), primary key(prof_name));
create table course(course_name varchar(20), dept_name varchar(20) references department, prof_name varchar(20) references professor(prof_name), primary key(course_name));
create table my_result(result_id serial, course_name varchar(20) references course(course_name), id varchar(20) references info(id), primary key(result_id));


insert into info values('jaewon', '1234');
insert into info values('1', '1');

insert into department values('Comp. Sci.', 'Informatics');
insert into department values('Business', 'Business');
insert into department values('English', 'Liberal');
insert into department values('Math', 'Science');

insert into professor values('Kim', 'Comp. Sci.');
insert into professor values('Yoo', 'Comp. Sci.');
insert into professor values('Chung', 'Comp. Sci.');
insert into professor values('Baek', 'Comp. Sci.');
insert into professor values('Lee', 'Comp. Sci.');
insert into professor values('Choi', 'Math');

insert into course values('Computer Network', 'Comp. Sci.', 'Kim');
insert into course values('Operating System', 'Comp. Sci.', 'Yoo');
insert into course values('Database', 'Comp. Sci.', 'Chung');
insert into course values('Logic Design', 'Comp. Sci.', 'Baek');
insert into course values('Engineering Circuits', 'Comp. Sci.', 'Lee');
insert into course values('Deep Learning', 'Comp. Sci.', 'Baek');
insert into course values('Calculus', 'Math', 'Choi');
insert into course values('AI', 'Comp. Sci.', 'Kim');







