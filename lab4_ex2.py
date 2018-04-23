from telegram.ext import CommandHandler, Updater, MessageHandler, Filters
from telegram import ChatAction
import pymysql


#import the list of tasks from the database
def read():
    sql = "SELECT todo from task"
    connection = pymysql.connect(user="root", password="root", host="localhost", database="taskmanager")
    cursor = connection.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    tasks = []
    for task in result:
        end = len(task)-2
        #taskk = task[2:end]
        print(task[0])
        tasks.append(task[0])
    print(result)
    cursor.close()
    connection.close()
    return tasks


def save(newTask):
    sql = "INSERT into task(todo) VALUES (%s)"
    connection = pymysql.connect(user="root", password="root", host="localhost", database="taskmanager")
    cursor = connection.cursor()
    cursor.execute(sql, (newTask,))
    connection.commit()
    cursor.close()
    connection.close()


def remove(task):
    sql = "DELETE FROM task WHERE todo=%s"
    connection = pymysql.connect(user="root", password="root", host="localhost", database="taskmanager")
    cursor = connection.cursor()
    cursor.execute(sql, (task,))
    connection.commit()
    cursor.close()
    connection.close()


def start(bot, update):
    update.message.reply_text("Hello!")
    print("Hello!")
    showCommands(bot, update)


def showCommands(bot, update):
    bot.sendChatAction(update.message.chat_id, ChatAction.TYPING)
    update.message.reply_text("1. /showTasks\n" + "2. /newTask <task to add>\n"
    + "3. /removeTask <task to remove>\n" + "4. /removeAllTasks <substring to use to remove all the tasks that contain it>\n"
    + "or /start or /stop")


def showTasks(bot, update):
    bot.sendChatAction(update.message.chat_id, ChatAction.TYPING)
    update.message.reply_text("The tasks you have planned are:")

    result = read()
    if len(result) == 0:
        bot.sendChatAction(update.message.chat_id, ChatAction.TYPING)
        update.message.reply_text("Nothing to do, here!")
    else:
        print(result)
        result.sort()
        for task in result:
            bot.sendChatAction(update.message.chat_id, ChatAction.TYPING)
            update.message.reply_text(task)

    showCommands(bot, update)


def newTask(bot, update, args):
    #new = update.message.text
    print(args)
    new = ""
    for word in args:
        new = new + word + " "
    save(new)

    bot.sendChatAction(update.message.chat_id, ChatAction.TYPING)
    update.message.reply_text("The new task was successfully added to the list!")

    showCommands(bot, update)


def removeTask(bot, update, args):
    rem = ""
    for word in args:
        rem = rem + word
        if args.index(word) < (len(args)-1):
            rem = rem + " "
    result = read()
    if rem in result:
        remove(rem)
        bot.sendChatAction(update.message.chat_id, ChatAction.TYPING)
        update.message.reply_text("The task was successfully deleted!")
    else:
        bot.sendChatAction(update.message.chat_id, ChatAction.TYPING)
        update.message.reply_text("The task you specified is not in the list!")
    showCommands(bot, update)


def removeAllTasks(bot, update, args):
    #only removes the task with the first occurrence of the word
    rem = args[0]
    print(rem)
    removed = []
    result = read()
    for task in result:
        if task.find(rem) != -1:
            removed.append(task)
            print(task)
            remove(task)

    if len(removed) > 0:
        string = "The elements "
        for old in removed:
            string = string + "\"" + old + "\" "
            if removed.index(old) < (len(removed)-1) :
                string = string + "and "
        string = string + "were successfully removed!"
        bot.sendChatAction(update.message.chat_id, ChatAction.TYPING)
        update.message.reply_text(string)
    else:
        bot.sendChatAction(update.message.chat_id, ChatAction.TYPING)
        update.message.reply_text("I did not find any task to delete!")
    showCommands(bot, update)


def stop(bot, update):
    bot.sendChatAction(update.message.chat_id, ChatAction.TYPING)
    update.message.reply_text("Bye bye!")
    exit(0)


def error(bot, update):
    bot.sendChatAction(update.message.chat_id, ChatAction.TYPING)
    update.message.reply_text("I'm sorry, I can't do that.")
    showCommands(bot, update)


def main():
    updater = Updater("500897023:AAFgIl4FC5PcsZU-KxZCTpNrx5TULx7xYTU")

    # register a command handler
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("showTasks", showTasks))
    dp.add_handler(CommandHandler("newTask", newTask, pass_args=True))
    dp.add_handler(CommandHandler("removeTask", removeTask, pass_args=True))
    dp.add_handler(CommandHandler("removeAllTasks", removeAllTasks, pass_args=True))
    dp.add_handler(CommandHandler("stop", stop))    #does not stop the program if /stop from telegram

    # add a non-command handler (messagge handler)
    dp.add_handler(MessageHandler(Filters.text, error))

    updater.start_polling()

    updater.idle()  # handle the stop of the program


if __name__ == "__main__":
    main()