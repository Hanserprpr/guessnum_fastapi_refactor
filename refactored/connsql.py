import mysql.connector
import re
from datetime import datetime


# 数据库配置
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "egg10052005",
    "database": "games_test"
}


class Connsql:
    def __init__(self, id, name, email, passwd, QQ):
        self.conn = mysql.connector.connect(**db_config)
        self.cursor = self.conn.cursor()


    def signup(self, name, email, sex, passwd, QQ):
        
        try:
            self.cursor.execute('''
            INSERT INTO users (name, email, sex, passwd, QQ)
            VALUES (%s, %s, %s, %s, %s)
            ''', (name, email, sex, passwd, QQ))
            self.conn.commit()
        except mysql.connector.IntegrityError as e:
            print(f"Error: {e}")
        finally:
            self.conn.close()

    # 查找密码
    def search_passwd(self,identifier: str):
        

        # 判断 identifier 是否是邮箱
        if re.match(r"[^@]+@[^@]+\.[^@]+", identifier):
            self.cursor.execute('''
            SELECT passwd
            FROM users
            WHERE email = %s
            ''', (identifier,))
        else:
            self.cursor.execute('''
            SELECT passwd
            FROM users
            WHERE name = %s
            ''', (identifier,))

        result = self.cursor.fetchone()
        self.conn.close()

        if result:
            return result[0]
        return None

    # 注册用户
    def signup(self, name: str, email: str, sex: str, passwd: str, QQ: str):   
        try:
            self.cursor.execute('''
            INSERT INTO users (name, email, sex, passwd, QQ)
            VALUES (%s, %s, %s, %s, %s)
            ''', (name, email, sex, passwd, QQ))
            self.conn.commit()
        except mysql.connector.IntegrityError as e:
            print(f"Error: {e}")
        finally:
            self.conn.close()

    # 查找密码
    def search_passwd(self, identifier: str):
        

        # 判断 identifier 是否是邮箱
        if re.match(r"[^@]+@[^@]+\.[^@]+", identifier):
            self.cursor.execute('''
            SELECT passwd
            FROM users
            WHERE email = %s
            ''', (identifier,))
        else:
            self.cursor.execute('''
            SELECT passwd
            FROM users
            WHERE name = %s
            ''', (identifier,))

        result = self.cursor.fetchone()
        self.conn.close()

        if result:
            return result[0]
        return None

    #查找用户id
    def search_id(self, name: str = None, QQ: str = None, email: str = None):
        
        if name:
            self.cursor.execute('''
                SELECT id
                FROM users
                WHERE name = %s
                ''', (name,))
        elif QQ:
            self.cursor.execute('''
                SELECT id
                FROM users
                WHERE QQ = %s
                ''', (QQ,))
        elif email:
            self.cursor.execute('''
                SELECT id
                FROM users
                WHERE email = %s
                ''', (email,))
        result = self.cursor.fetchone()
        self.conn.close()
        if result:
            return result[0]
        else:
            return None


    #查找用户名
    def search_name(self, QQ: str = None, user_id: int = None):
        if not QQ and not user_id:
            raise ValueError("必须提供QQ号或用户ID之一进行查询。")

        

        # 优先根据 QQ 进行查询，如果没有则使用 user_id
        if QQ:
            self.cursor.execute('''
                SELECT name
                FROM users
                WHERE QQ = %s
            ''', (QQ,))
        elif user_id:
            self.cursor.execute('''
                SELECT name
                FROM users
                WHERE id = %s
            ''', (user_id,))

        result = self.cursor.fetchone()
        self.conn.close()

        if result:
            return result[0]
        else:
            return None

    #查找用户个人信息
    def get_me(self, QQ:str = None, user_id:str = None):
        
        if not QQ and not user_id:
            raise ValueError("必须提供QQ号或用户ID之一进行查询。")
        if QQ:
            self.cursor.execute('''
                SELECT *
                FROM users
                WHERE QQ = %s
                ''', (QQ,))
        elif user_id:
            self.cursor.execute('''
                SELECT *
                FROM users
                WHERE id = %s
            ''', (user_id,))

        result = self.cursor.fetchone()
        self.conn.close()
        user_id, name, email, sex, _, qq, status, created_at, updated_at, last_login = result
        
        # 格式化个人中心信息
        return (
            f"用户 ID: {user_id}\n"
            f"用户名: {name}\n"
            f"邮箱: {email}\n"
            f"性别: {'男' if sex == 'M' else '女' if sex == 'F' else '其他'}\n"
            f"QQ: {qq}\n"
            f"账号状态: {'活跃' if status == 1 else '禁用'}\n"
            f"注册时间: {created_at.strftime('%Y-%m-%d %H:%M:%S')}\n"
            f"最后更新时间: {updated_at.strftime('%Y-%m-%d %H:%M:%S')}\n"
            f"最后登录时间:{last_login.strftime('%Y-%m-%d %H:%M:%S')}"
        )




    # 更新用户最后登录时间
    def update_last_login(self, QQ: str = None, user_id : str = None):
        
        try:
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            if QQ:
                self.cursor.execute('''
                    UPDATE users
                    SET last_login = %s
                    WHERE QQ = %s
                ''', (current_time, QQ))
                self.conn.commit()
            elif user_id:
                self.cursor.execute('''
                    UPDATE users
                    SET last_login = %s
                    WHERE id = %s
                ''', (current_time, user_id))
                self.conn.commit()
        except mysql.connector.Error as e:
            print(f"Error: {e}")
        finally:
            self.conn.close()

    #更新用户信息
    def update_user_info(self, qq: str, name: str = None, passwd: str = None, sex: str = None):
        
        try:
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            if name:
                self.cursor.execute('''
                    UPDATE users
                    SET name = %s, updated_at = %s
                    WHERE QQ = %s
                ''', (name, current_time, qq))
            if passwd:
                self.cursor.execute('''
                    UPDATE users
                    SET passwd = %s, updated_at = %s
                    WHERE QQ = %s
                ''', (passwd, current_time, qq))
            if sex:
                self.cursor.execute('''
                    UPDATE users
                    SET sex = %s, updated_at = %s
                    WHERE QQ = %s
                ''', (sex, current_time, qq))
            self.conn.commit()
        except mysql.connector.Error as e:
            print(f"Error: {e}")
        finally:
            self.conn.close()


    def get_id(self, qq:str):
        
        self.cursor.execute('''
        SELECT id
        FROM users
        where QQ = %s
        ''', (qq,))
        result = self.cursor.fetchone()
        self.conn.close()
        
        return result[0] if result else None



    def save_game_attempt(self, user_id, game_name, score, attempts):
        
        self.cursor.execute("""
            INSERT INTO game_attempts (user_id, game_name, score, attempts, result)
            VALUES (%s, %s, %s, %s, %s)
        """, (user_id, game_name, score, attempts, 'win'))
        self.conn.commit()
        self.cursor.close()
        self.conn.close()

    def update_user_stats(self, user_id, game_name, score, attempts):
        
        # 检查 `game_stats` 中是否已有记录
        self.cursor.execute("""
            SELECT * FROM game_stats WHERE user_id = %s AND game_name = %s
        """, (user_id, game_name))
        result = self.cursor.fetchone()

        if result:
            # 更新现有记录
            self.cursor.execute("""
                UPDATE game_stats
                SET total_score = total_score + %s,
                    games_played = games_played + 1,
                    average_score = (total_score + %s) / (games_played + 1),
                    min_attempts = LEAST(min_attempts, %s),
                    max_attempts = GREATEST(max_attempts, %s),
                    play_count = play_count + 1,
                    last_played = NOW()
                WHERE user_id = %s AND game_name = %s
            """, (score, score, attempts, attempts, user_id, game_name))
        else:
            # 插入新的记录
            self.cursor.execute("""
                INSERT INTO game_stats (user_id, game_name, total_score, games_played, average_score, 
                                        wins, play_count, min_attempts, max_attempts, last_played)
                VALUES (%s, %s, %s, 1, %s, 1, 1, %s, %s, NOW())
            """, (user_id, game_name, score, score, attempts, attempts))

        self.conn.commit()
        self.cursor.close()
        self.conn.close()



    def fetch_game_history(self, user_id, game_name):
        # 获取用户的游戏历史记录
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)
        
        # 查询游戏历史记录
        self.cursor.execute("""
            SELECT attempts, score, played_at
            FROM game_attempts
            WHERE user_id = %s AND game_name = %s
            ORDER BY played_at DESC
            LIMIT 10;
        """, (user_id, game_name))
        
        history = cursor.fetchall()
        self.cursor.close()
        self.conn.close()
        
        return history

    def fetch_leaderboard(self, game_name):
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)

        # 获取按平均分数排行的前 10 名
        self.cursor.execute("""
            SELECT user_id, average_score
            FROM game_stats
            WHERE game_name = %s
            ORDER BY average_score DESC
            LIMIT 10;
        """, (game_name,))
        
        leaderboard = cursor.fetchall()
        self.cursor.close()
        self.conn.close()
        
        return leaderboard

    import mysql.connector

    def get_user_rank(self, user_id, game_name):
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)

        
        # 查询用户的当前排名
        self.cursor.execute("""
            SELECT ranking, user_id, average_score
            FROM (
                SELECT user_id, average_score,
                    RANK() OVER (ORDER BY average_score DESC) AS ranking
                FROM game_stats
                WHERE game_name = %s
            ) AS ranked_stats
            WHERE user_id = %s;
        """, (game_name, user_id))
        
        user_rank = self.cursor.fetchone()
        if cursor.with_rows:
            cursor.fetchall() 

        self.cursor.close()
        self.conn.close()
        
        return user_rank
