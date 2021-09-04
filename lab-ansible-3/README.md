# Ansible Lab #3 - 把查询到的信息导出为Excel文件，并以邮件形式发送

<br><br>

## Lab 步骤

<br>

1. 查看 main.yml 文件内容


```yaml
  vars:
    apic_info: &apic_info
      host:           "{{ aci_host }}"
      user:           "{{ aci_user }}"
      password:       "{{ aci_password }}"
      validate_certs: "{{ aci_valid_cert }}" 
      use_ssl:        "{{ aci_use_ssl }}" 

  tasks:
    - name: "1] API Request - 读取所有接口的状态信息"
      aci_rest:
        <<: *apic_info
        path: /api/class/ethpmPhysIf.json
        method: get
      register: ethpmPhysIf
```
- 通过 YAML Anchor(&) 可以重复使用变量内容
- 通过调用 ethpmPhysIf class，读取所有interface的信息

<br><br>

2. 查看 Playbook 文件(main.yml) 内容。

```yaml
    - name: "2] API Request - 查询所有接口目录信息"
      aci_rest:
        <<: *apic_info
        path: /api/class/l1PhysIf.json?page-size=10     # page-size 限制返回值大小
        method: get
      register: l1PhysIf

    - name: "3] API Request - 搜集所有接口故障数值信息"
      aci_rest:
        <<: *apic_info
        path: "/api/node/mo/{{ item }}.json?query-target=children&target-subtree-class=rmonDot3Stats&target-subtree-class=rmonDot1d&target-subtree-class=rmonEtherStats"
        method: get
      register: rmonEtherStats
      with_items:
        - "{{ l1PhysIf | json_query('imdata[].l1PhysIf.attributes.dn') }}"
```
- 通过 l1PhysIf class， 搜集所有接口目录信息。(page-size=10 表示只搜集10个接口信息。)
- 针对搜集到的接口信息，在Task 3中，对每个接口是否有报错信息进行查验。通过接口的MO，查询其Child Class中的rmonDot3Stats, rmonDot1d, rmonEtherStats的信息来判断接口是否有错误。

<br><br>

3. 把1和2中搜集的数据（ethpmPhysIf, rmon）以JSON文件的形式存储。

```yaml
    - name: "4] 以JSON的形式存储"
      copy:
        content: "{{ item.content | to_nice_json}}"
        dest:    "{{ item.dest }}"
      no_log: yes
      loop:
        - content:  "{{ ethpmPhysIf | json_query('imdata[].ethpmPhysIf.attributes.{dn:dn, operSt:operSt, operMode:operMode, operSpeed:operSpeed, operDuplex:operDuplex}') }}"
          dest:     interface_status.json
        - content:  "{{ rmon | json_query('results[].{item:item, imdata:imdata[]}') }}" 
          dest:     interfaces_error_counters.json
```
- 通过json_query，把数据（ethpmPhysIf, rmon）中特定的信息存储到JSON文件中。
- no_log: yes 表示不在console中显示log。

<br><br>

4. 执行Playbook，查看生成的JSON文件。
```
ansible-playbook -i hosts main.yml
```
![](../images/lab-ansible-3/lab-ansible-3-1.png)

<br><br>

5. 通过Python，查询报错信息，并把JSON文件导出为Excel文件。

```yaml
    - name: "5] JSON 导出为 Excel文件（使用Python）"
      command: python3 files/"{{ item }}"
      loop:
        - json2xlsx.py
        - json2xlsx_err.py
```
- json2xlsx.py 是把 interface_status.json 文件转换为Excel。
- json2xlsx_err.py 是把 interfaces_error_counters.json 文件转换为Excel。

<br><br>

6. 执行Playbook，查看生成的Excel文件。
```
ansible-playbook -i hosts main.yml
```

- 生成2个Excel。

![](../images/lab-ansible-3/lab-ansible-3-2.png)

<br><br>

7. 添加发送邮件Task。

```yaml
    - name: "6] 把 Excel 文件通过以附件形式发送"
      mail:
        host:     "{{ outlook_host }}"
        port:     "{{ outlook_port }}"
        username: "{{ outlook_username }}"
        password: "{{ outlook_password }}"
        from:     "{{ outlook_username }}"
        to :      "{{ outlook_receiver }}"
        subject:  "CISCO ACI 接口状态、错误报告"
        subtype:  html
        body:     "{{ outlook_body }}"
        secure:   starttls
        headers:  "Content-type=text/html"
        attach: 
          - "./接口_状态.xlsx"
          - "./接口_错误.xlsx"
```

<br><br>

8. 在Inventory文件中修改邮箱信息。

```
[aci:vars]
...

outlook_host="smtp.office365.com"
outlook_port=587
outlook_username="cuijian0505@hotmail.com"
outlook_password="CHANGE_ME"
outlook_from="cuijian0505@hotmail.com"
outlook_receiver="jiacui@cisco.com"
outlook_body="..."
```
- 修改 outlook_password 的 "CHANGE_ME" 值为实际密码。
- 修改 outlook_receiver 的值为邮件接收方地址。 

<br><br>

9. 执行Playbook，查看是否接收邮件。
```
ansible-playbook -i hosts main.yml
```

<br><br>

# 参考文档：
- Ansible anchor: https://docs.ansible.com/ansible/latest/user_guide/playbooks_advanced_syntax.html#yaml-anchors-and-aliases-sharing-variable-values
