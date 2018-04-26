# encoding=utf-8

import pymysql

class sqltool:

    def safe(self,s):
        return pymysql.escape_string(s)


    def get_i_sql(self,table, dict):
        '''
           生成insert的sql语句
           @table，插入记录的表名
           @dict,插入的数据，字典
           '''
        sql = 'insert into %s set ' % table
        sql += self.dict_2_str(dict)
        return sql

    #插入去重的语句
    def get_ignore_i_sql(self,table,dict):
        sql = 'insert IGNORE into %s set ' % table
        sql += self.dict_2_str(dict)
        return sql



    def get_s_sql(self,table, keys, conditions, isdistinct=0):
        '''
            生成select的sql语句
        @table，查询记录的表名
        @key，需要查询的字段
        @conditions,插入的数据，字典
        @isdistinct,查询的数据是否不重复
        '''
        if isdistinct:
            sql = 'select distinct %s ' % ",".join(keys)
        else:
            sql = 'select  %s ' % ",".join(keys)
        sql += ' from %s ' % table
        if conditions:
            sql += ' where %s ' % self.dict_2_str_and(conditions)
        return sql

    def get_s_sql_like(self,table,keys,likedict,conditions,isdistinct=0):
        if isdistinct:
            sql = 'select distinct %s ' % ",".join(keys)
        else:
            sql = 'select  %s ' % ",".join(keys)
        sql += ' from %s ' % table
        if conditions:
            sql += ' where %s ' % self.dict_2_str_like(conditions,likedict)
        return sql

    def get_count_sql(self,table, conditions,like={}, isdistinct=0):
        '''
            生成select的sql语句
        @table，查询记录的表名
        @key，需要查询的字段
        @conditions,插入的数据，字典
        @isdistinct,查询的数据是否不重复
        '''
        if isdistinct:
            sql = 'select COUNT(*) distinct '
        else:
            sql = 'select COUNT(*) '
        sql += ' from %s ' % table
        if conditions:
            sql += ' where %s ' % self.dict_2_str_like(conditions,like)
        return sql


    def get_u_sql(self,table, value, conditions):
        '''
            生成update的sql语句
        @table，查询记录的表名
        @value，dict,需要更新的字段
        @conditions,插入的数据，字典
        '''
        sql = 'update %s set ' % table
        sql += self.dict_2_str(value)
        if conditions:
            sql += ' where %s ' % self.dict_2_str_and(conditions)
        return sql


    def get_d_sql(self,table, conditions):
        '''
            生成detele的sql语句
        @table，查询记录的表名

        @conditions,插入的数据，字典
        '''
        sql = 'delete from  %s  ' % table
        if conditions:
            sql += ' where %s ' % self.dict_2_str_and(conditions)
        return sql

    def dict_2_conditions(self,conditions,like={}):
        sql=""
        sql += ' where %s ' % self.dict_2_str_like(conditions,like)

    def dict_2_str(self,dictin):
        '''
        将字典变成，key='value',key='value' 的形式
        '''
        tmplist = []
        for k, v in dictin.items():
            tmp = "%s='%s'" % (str(k), self.safe(str(v)))
            tmplist.append(' ' + tmp + ' ')
        return ','.join(tmplist)


    def dict_2_str_and(self,dictin):
        '''
        将字典变成，key='value' and key='value'的形式
        '''
        tmplist = []
        for k, v in dictin.items():
            tmp = "%s='%s'" % (str(k), self.safe(str(v)))
            tmplist.append(' ' + tmp + ' ')
        return ' and '.join(tmplist)

    def dict_2_str_like(self,dictin,like={}):
        '''
        将字典变成，key='value' and key like 'value'的形式
        '''
        tmplist = []
        for k, v in dictin.items():
            if like.get(str(k))=='1':
                tmp = "%s like '%s'" % (str(k), self.safe("%"+str(v)+"%"))
            else:
                tmp = "%s='%s'" % (str(k), self.safe(str(v)))
            tmplist.append(' ' + tmp + ' ')
        return ' and '.join(tmplist)