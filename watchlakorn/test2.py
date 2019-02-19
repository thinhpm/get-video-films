import requests

par = {}

re = requests.post('http://analysis-center.local/wp-admin/admin-ajax.php', data={
  "action": "set_voucher",
  "data": {
      "1": 'h2',
      "23": 'h1'
  }
})

print(re.content)