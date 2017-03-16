--
-- userid: user id
-- reg_date: registration date
-- lASt_login: date of lASt login
-- logins_7d: number of the pASt 7 days for which the user hAS logged in (should be a value 0-7)
-- logins_7d_mobile: number of the pASt 7 days for which the user hAS logged in on mobile
-- logins_7d_web: number of the pASt 7 days for which the user hAS logged in on web
-- opt_out: whether or not the user hAS opted out of receiving email

SELECT
  reg.userid,
  reg.tmstmp AS registration_date,
  max(l.tmstmp) AS last_login,
  count(l.userid) AS logins_7d,
  sum(CASE WHEN
    l.type='mobile' AND l.tmstmp BETWEEN timestamp '2014-08-14' - interval '7 days' AND '2014-08-14'
      THEN 1
    ELSE 0
  END) AS logins_7d_mobil,
  sum(CASE WHEN
    l.type='web' AND l.tmstmp BETWEEN timestamp '2014-08-14' - interval '7 days' AND '2014-08-14'
      THEN 1
    ELSE 0
  END) AS logins_7d_web,
  (reg.userid IN (SELECT userid FROM optout)) AS opt_out
FROM registrations reg
LEFT JOIN logins l ON l.userid=reg.userid
GROUP BY reg.userid, reg.tmstmp
ORDER BY logins_7d;
LIMIT 5;


select timestamp '2014-08-06' BETWEEN timestamp '2014-08-14' - interval '7 days' AND '2014-08-14' ;
select * from logins limit 5;
select (userid in (select userid from optout)) from registrations;

SELECT userid, COUNT(*) AS cnt, timestamp %(ts)s AS date_7d
      FROM logins
      WHERE logins.tmstmp > timestamp %(ts)s - interval '7 days'
      GROUP BY userid;''', {'ts': ts}
