database_config = {    
    'server_name' :'localhost',
    'port' : '5432',
    'database_name' : 'CastingDB',
    'user_name' : 'postgres', 
    'password' : 'huangqi861012'
}

ROWS_PER_PAGE = 10

auth0_config = {
    'AUTH0_DOMAIN' : 'huangqiron.us.auth0.com',
    'ALGORITHMS' : ['RS256'],
    'API_AUDIENCE' : 'Casting'
}

auth0_login_url = 'https://huangqiron.us.auth0.com/authorize?audience=Casting&response_type=token&client_id=4I1aGDGMSjfXyLlFX5SObhcYio9EFOTJ&redirect_uri=http://localhost:8080/login-results'

tesing_account = {
    'casting_staff' : {'username' : 'castingstaff@casting.com', 'password' : '!AMcastingstaff'},
    'casting_director' : {'username' : 'castingdirector@casting.com', 'password' : '!AMcastingdirector'}
}

auth_header = {
    'casting_staff': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InJfYWVTeW1oaERMQTV5OC1xTDBzdiJ9.eyJpc3MiOiJodHRwczovL2h1YW5ncWlyb24udXMuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVmNjFjMmRjNWZlYTc2MDA2YjA4ZjhlZCIsImF1ZCI6IkNhc3RpbmciLCJpYXQiOjE2MDAzMDUxODcsImV4cCI6MTYwMDMxMjM4NywiYXpwIjoiNEkxYUdER01TamZYeUxsRlg1U09iaGNZaW85RUZPVEoiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIl19.MvHkWqmLrTGu6IB6iTbLNe5hxddeTqifzI_fCAdmw_Ujwr7MbM230p8IzEFokeHZkApft4Jt-3i1ON4AcTnNQATgw2uelUNFdj0NRtOMJD_pU9Hlvriu5VLdtJnbf4kAr6z4S6VC8B86FtulOzcBCnCIc4as9HU485YiD-g7I7tridKZhxi25AzZU124Omz_NZDda3LZno1u9nezW6YngT2Xo6X_i8EiSeLoameJAGJiDexodUT2BMmgO04pXLHu2uYLiK4_JCmLvqOkm8I_CXZhmfRAJn2vj44BPS9dSGb6--rIwIX_cM2dFBkVq3NXoekFgX-lYjWvBgn84mM9XQ',
    'casting_director':'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InJfYWVTeW1oaERMQTV5OC1xTDBzdiJ9.eyJpc3MiOiJodHRwczovL2h1YW5ncWlyb24udXMuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVmNjFjMjRmYzBlNTllMDA3NmYxYjE3NyIsImF1ZCI6IkNhc3RpbmciLCJpYXQiOjE2MDAzMDIyMTYsImV4cCI6MTYwMDMwOTQxNiwiYXpwIjoiNEkxYUdER01TamZYeUxsRlg1U09iaGNZaW85RUZPVEoiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvcnMiLCJkZWxldGU6bW92aWVzIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvcnMiLCJwYXRjaDptb3ZpZXMiLCJwb3N0OmFjdG9ycyIsInBvc3Q6bW92aWVzIl19.pc8M3AAyrluXSu24licsSlwENgxakzUz2iYai-8mPFp6PxtCK97DuZZlG7Iy39jjmNtAqSCgOs0j_x0UgXJ4AtpnJKPL7gBSXJXWc6MI8gkEKCyALyBV0CdiyK4rcVz596jRTwmkhEGRSs18XBXVSiXJAh_ttW4rS5qYzU9LPvDatUX4LmWxvcCGgCXOMqs-Zu5GQeHrXQfbo1fWJi36sX91SToVsD-w3ybZwyO36SWwFWOs6fHVq1bZiC0x6cOlQhwGkV9RXJvqw-U9Hf92Vc_sziAohXRoef-_l1RMKCQU8RekySdEJg2_nkWP-QyeeLF4ZNSu7XMj_n2KsFVl8Q'
}
