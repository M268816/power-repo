class Main:    
    def my_func():
        print('Function')
        
        def my_method():
            print('Method')
            
        my_method()
    
if __name__ == '__main__':
    Main.my_func()