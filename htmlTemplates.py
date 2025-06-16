css = '''
<style>
.chat-message {
    padding: 1.5rem;
    border-radius: 10px;
    margin-bottom: 1rem;
    display: flex;
    align-items: center;
}
.chat-message.user {
    background-color: #DCF8C6;
    justify-content: flex-end;
}
.chat-message.bot {
    background-color: #F1F0F0;
    justify-content: flex-start;
}
.chat-message img {
    max-width: 30px;
    margin-right: 10px;
}
</style>
'''

bot_template = '''
<div class="chat-message bot">
    <img src="https://cdn-icons-png.flaticon.com/512/4712/4712109.png" alt="bot icon">
    <div>{message}</div>
</div>
'''

user_template = '''
<div class="chat-message user">
    <div>{message}</div>
    <img src="https://cdn-icons-png.flaticon.com/512/847/847969.png" alt="user icon">
</div>
'''
