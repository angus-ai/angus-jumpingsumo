# -*- coding: utf-8 -*-
#!/usr/bin/env python

# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

import os
import subprocess
import threading
import time
import angus


WIDTH = 640


def img_generator(file_path):
    with open(file_path, "rb") as f:
        buff = ""
        for chunk in f:
            buff += chunk
            s = buff.find('\xff\xd8')
            e = buff.find('\xff\xd9')
            if s != -1 and e != -1:
                jpg = buff[s:e + 2]
                buff = buff[e + 2:]
                yield jpg


def command(img, service):
    file_path = '/tmp/imgtmp.jpg'

    with open(file_path, 'wb') as f:
        f.write(img)

    job = service.process({'image': open(file_path, 'rb')})

    result = job.result['faces']

    if len(result) > 0 and result[0]['roi_confidence'] > 0.5:
        roi = result[0]['roi']

        x = roi[0]
        w = roi[2]
        cmd_angle = (x + w * 0.5) - WIDTH / 2

        print w
        if abs(cmd_angle) > WIDTH / 8:
            if cmd_angle > 0:
                return "Right"
            else:
                return "Left"
        elif w > 100:
            return "Back"
        elif w < 80:
            return "Forw"
    return None


def command_loop(singleton, sub, service):
    img = singleton[0]
    if img is None:
        return

    cmd = command(img, service)
    if cmd == "Right":
        sub.stdin.write("u")
        sub.stdin.flush()
    elif cmd == "Left":
        sub.stdin.write("y")
        sub.stdin.flush()
    elif cmd == "Back":
        sub.stdin.write("i")
        sub.stdin.flush()
    elif cmd == "Forw":
        sub.stdin.write("o")
        sub.stdin.flush()


def loop(singleton, sub, service):
    while True:
        command_loop(singleton, sub, service)
        # print "Loop"
        time.sleep(1)


def launch(input_path, sub, service):
    singleton = [None]
    count = 0
    thread = threading.Thread(target=loop, args=(singleton, sub, service))
    thread.daemon = True
    thread.start()

    for img in img_generator(input_path):
        singleton[0] = img
        count += 1
        if count > 600:
            break

    sub.stdin.write("q")
    sub.stdin.flush()


def main():
    os.environ[
        'LD_LIBRARY_PATH'] = "../ARSDKBuildUtils/Targets/Unix/Install/lib"
    sub = subprocess.Popen(
        ["./JumpingSumoInterface"],
        stdin=subprocess.PIPE,
        stdout=None,
        stderr=subprocess.STDOUT)
    time.sleep(2)
    conn = angus.connect()
    service = conn.services.get_service('face_detection', 1)
    launch("./video_fifo", sub, service)

if __name__ == "__main__":
    main()
