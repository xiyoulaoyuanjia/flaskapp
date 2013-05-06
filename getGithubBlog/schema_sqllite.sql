drop table if exists blog_entries;
create table blog_entries (
		  id integer primary key autoincrement,
		  title string not null,
		  text  string ,
		  href  string not null,
		  oriId    string,
	      des      string not null	
);
