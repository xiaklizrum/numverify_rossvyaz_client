
CREATE TABLE `phone_codes`(
	`id`      Integer NOT NULL PRIMARY KEY AUTOINCREMENT,
	`code`    Integer,
	`begin`   Integer NOT NULL,
	`end`     Integer NOT NULL,
	`count`   Integer,
	`carrier` Text,
	`city`    Text,
	`region`  Text
)