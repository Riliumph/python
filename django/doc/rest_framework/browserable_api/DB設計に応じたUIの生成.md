# Browsable APIのUI

## auto_now_addフィールドは作られない

![auto_now_add](./img/auto_now_add.png)

`auto_now_add`フラグがレコードが追加されるときのみ機能して値が付与される。  
つまり、基本的には変更を許容しないカラムである。  
そのため、Browsable APIのUIではテキストボックスが表示されない
