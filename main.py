import pymysql
import vk_api, json
from vk_api.utils import get_random_id
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType


vk_session = vk_api.VkApi(token='b24c75efd7a985cbeed15f42c275927b5061a99d8a6e89e2ef850bfc8eea6f874125ea9c2c319225b273a')
longpoll = VkBotLongPoll(vk_session, '202850434')
vk = vk_session.get_api()

con = pymysql.connect(host='localhost',
                      user='root',
                      password='2012-2020',
                      db='new_schema', )
print("connect successful!!")


cur = con.cursor()
cur.execute("SELECT login,password FROM Student")
listRows = cur.fetchall()
listLogPas = []

def get_but(text, color):
    return {
        "action": {
            "type": "text",
            "payload": "{\"button\": \"" + "1" + "\"}",
            "label": f"{text}"
        },
        "color": f"{color}"
    }

object1 = con.cursor()
object2 = con.cursor()
def main():
    InputLogin = False
    InputPassword = False
    AllRight = False
    MarkRight = False

    for event in longpoll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW and InputLogin==False:
            vk.messages.send(
                user_id=event.obj.from_id,
                random_id=get_random_id(),
                message=("Введите свой логин"),
                keyboard=emptyKeyboard,
            )
            InputLogin=True

        elif event.type == VkBotEventType.MESSAGE_NEW and InputLogin==True and InputPassword==False:
            listLogPas.append(event.obj.text)
            vk.messages.send(
                user_id=event.obj.from_id,
                random_id=get_random_id(),
                message=("Введи свой пароль")
            )
            InputPassword=True

        elif event.type == VkBotEventType.MESSAGE_NEW and InputLogin==True and InputPassword==True and AllRight==False:
            listLogPas.append(event.obj.text)
            if tuple(listLogPas) in listRows:
                vk.messages.send(
                    user_id=event.obj.from_id,
                    random_id=get_random_id(),
                    message=("Все верно"),
                    keyboard = keyboard,
                )
                AllRight=True
            else:
                vk.messages.send(
                    user_id=event.obj.from_id,
                    random_id=get_random_id(),
                    message=("Что то неверно")
                )
                listLogPas.clear()
                InputLogin=False
                InputPassword=False

        elif event.type == VkBotEventType.MESSAGE_NEW:  # ПЕРВЫЙ БЛОК КНОПОК

            if (event.obj.text == "оценить/написать отзыв"):

                object1.execute("""SELECT course_name FROM courses WHERE course_id IN  (SELECT course_id from student_course
                WHERE student_id IN (SELECT student_id from student where login = %s and password = %s ));""", (listLogPas[0],listLogPas[1]))
                ObjectRows = object1.fetchall()

                keyboardObjects = {
                    "one_time": False,
                    "buttons": [
                        [get_but(*ObjectRows[0], 'primary'), get_but(*ObjectRows[1], 'primary')],
                        [get_but('-', 'primary'), get_but('-', 'primary')]
                    ]
                }
                keyboardObjects = json.dumps(keyboardObjects, ensure_ascii=False).encode('utf-8')
                keyboardObjects = str(keyboardObjects.decode('utf-8'))

                vk.messages.send(
                    user_id=event.obj.from_id,
                    random_id=get_random_id(),
                    message=("Выбирай предмет"),
                    keyboard=keyboardObjects,
                )

            elif (event.obj.text == ObjectRows[0][0] or event.obj.text == ObjectRows[1][0]) and MarkRight == False:
                ObjectName = event.obj.text

                vk.messages.send(
                    user_id=event.obj.from_id,
                    random_id=get_random_id(),
                    message=("Введите оценку от 1 до 10"),
                    MarkRight = True
                )

            elif int(event.obj.text) > 0 and int(event.obj.text) <= 7:
                print(type(int(event.obj.text)), ObjectName)
                object2.execute("UPDATE `new_schema`.`courses` SET `course_mark` = %s WHERE (`course_name` = %s);",(int(event.obj.text), ObjectName))

            elif (event.obj.text == "оценить онлайн-курс"):
                vk.messages.send(
                    user_id=event.obj.from_id,
                    random_id=get_random_id(),
                    message=("Выбирай онлайн-курс"),
                    keyboard=emptyKeyboard,
                )

            elif (event.obj.text == "посмотреть оценку/отзыв"):
                vk.messages.send(
                    user_id=event.obj.from_id,
                    random_id=get_random_id(),
                    message=("Смотри оценку/отзыв"),
                    keyboard=emptyKeyboard,
                )

            elif (event.obj.text == "оценить куратора пп"):
                vk.messages.send(
                    user_id=event.obj.from_id,
                    random_id=get_random_id(),
                    message=("Выбирай куратора"),
                    keyboard=emptyKeyboard,
                )
            elif (event.obj.text == "Предмет1"):  # ВТОРОЙ БЛОК КНОПОК
                vk.messages.send(
                    user_id=event.obj.from_id,
                    random_id=get_random_id(),
                    message=("смотри инфу по предмет1"),
                    keyboard=emptyKeyboard,
                )


emptyKeyboard = {
    "one_time": False,
    "buttons": [
    ]
}

keyboard = {
    "one_time": False,
    "buttons": [
        [get_but('оценить/написать отзыв', 'primary'), get_but('оценить онлайн-курс', 'primary')],
        [get_but('посмотреть оценку/отзыв', 'primary'), get_but('оценить куратора пп', 'primary')]
    ]
}

keyboard = json.dumps(keyboard, ensure_ascii=False).encode('utf-8')
keyboard = str(keyboard.decode('utf-8'))

emptyKeyboard = json.dumps(emptyKeyboard, ensure_ascii=False).encode('utf-8')
emptyKeyboard = str(emptyKeyboard.decode('utf-8'))

if __name__ == '__main__':
    main()