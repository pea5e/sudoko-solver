from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep
import re
from time import time
from selenium.webdriver.chrome.options import Options


option = Options()
option.add_argument('--no-sandbox')
option.add_argument('--disable-dev-shm-usage')

browser = webdriver.Chrome(options=option)




def indicator(string,indicator="value"):
    patt = indicator+'\s*=\s*"(\d)\s*"'
    return(''.join(re.findall(patt ,string)))

class sudoko:

	def __init__(self,table):
		self.num_ins = 0
		self.grid = table.copy()
        

	def get_row(self,index):
		index -= 1
		self.row = self.grid[index]
		return(self.grid[index])

	def get_column(self,index):
		index -= 1
		self.column = [ ]
		for row in self.grid :
			self.column.append(row[index])
		return(self.column)

	def get_chart(self,index):
		index -= 1
		self.chart = [ ]
		for row in self.grid[(index//3)*3:(index//3)*3+3]:
			#self.chart.append([ ])
			for cell in row[(index%3)*3:(index%3+1)*3] :
				self.chart.append(cell)

		return(self.chart)

	def get_cell(self,row,column):
		return(self.grid[row-1][column-1])

	def puts(self,row,column,value):
		print('(',row,'-',column,') = ',value)
		self.grid[row-1][column-1] = value

	def put(self,row,column,value):
		table = browser.find_element_by_id('puzzle_grid')
		cell = table.find_element_by_id("c"+str(column-1)+str(row-1))
		cell.find_element_by_tag_name('input').send_keys(str(value))
		self.num_ins += 1
		print(self.num_ins,': (',row,',',column,') = ',value)
		self.grid[row-1][column-1] = value
		#self.puts(row,column,value)

	def left(self):
		left = 0
		for row in self.grid:
			left += num_left(row)
		return (left)

	def free(self,square_index):
		l = list()
		for i in range(len(self.get_chart(square_index))):
			if self.get_chart(square_index)[i] == 0:    
				row = (i//3)+((square_index-1)//3)*3
				column = (i%3)+((square_index-1)%3)*3
				l.append([row,column])
		return(l)


def free(item):
    l = list()
    for i in range(len(item)):
        if item[i] == 0:    l.append(i+1)
    return(l)


def num_left(item):
    return ( item.count(0))

def left(item):
    num = [1,2,3,4,5,6,7,8,9]
    for i in item:
        if i != 0 :
            num.remove(i)
    return (num)


def is_full(item):
        if 0 in item:
            return ( False )
        else:
            return ( True )

def chartsinrow(chart_index):
    l =  ([1,2,3,4,5,6,7,8,9][((chart_index-1)%3)::3]+[1,2,3,4,5,6,7,8,9][(chart_index-1)-((chart_index-1)%3):3+((chart_index-1)-((chart_index-1)%3))])
    l.remove(chart_index)
    l.remove(chart_index)
    return (l)

def open_sudoko(level = 1):
    browser.get("https://www.websudoku.com/?level="+str(level))
    browser.switch_to.frame(browser.find_element_by_tag_name('frame'))
    table = browser.find_element_by_id('puzzle_grid')
    rows = table.find_elements_by_tag_name('tr')
    grid = [ ]
    for row in rows:
        cells = row.find_elements_by_tag_name('td')
        grid.append([ ])
        for c in cells:
                value = indicator(str(c.get_attribute('innerHTML')))
                if value!='':
                    grid[rows.index(row)].append(int(value))
                else:
                    grid[rows.index(row)].append(0)
    return (grid)

'''
grid = [
    [6,9,0,4,2,1,8,7,0],
    [4,0,3,8,7,0,2,0,0],
    [0,7,2,0,0,3,4,0,1],
    [0,0,0,1,8,6,5,3,4],
    [1,5,6,7,3,4,0,0,0],
    [3,0,4,2,5,9,0,1,7],
    [0,0,0,0,0,7,1,8,5],
    [5,0,0,3,0,2,0,4,9],
    [7,0,0,5,9,8,3,0,0]
    ]

#my = sudoko(grid)


def methode1(my,row):
    if num_left(my.get_row(row+1)) == 1 :
        #
        #print('\n',my.get_row(row+1),num_left(my.get_row(row+1)),sep='\t')
        #
        my.put(row+1,my.get_row(row+1).index(0)+1,left(my.get_row(row+1))[0])
    if num_left(my.get_column(row+1)) == 1 :
        #
        #print('\n',my.get_column(row+1),num_left(my.get_column(row+1)),sep='\t')
        #
        my.put(my.get_column(row+1).index(0)+1,row+1,left(my.get_column(row+1))[0])
    if num_left(my.get_chart(row+1)) == 1 :
        #
        #print('\n',my.get_chart(row+1),num_left(my.get_chart(row+1)),sep='\t')
        #
        not_fulled = my.free(row+1)[0]
        my.put(not_fulled[0]+1,not_fulled[1]+1,left(my.get_chart(row+1))[0])


def methode2():
        
'''

my = sudoko(open_sudoko(1))

#print(my.grid)

#choose level { 1 , 2 , 3 , 4 } in open_sudoko as parameter

lefts = my.left()

start = time()
while my.left() > 0 :

    for row in range(9):
        #print(my.get_row(row+1),left(my.get_row(row+1)),sep="\n")
        for item in left(my.get_row(row+1)):
            possible = list()
            #print(item)
            for y in free(my.get_row(row+1)):
                if not item in my.get_column(y):
                    #print(item," not in column",y);
                    #input()
                    if len(possible)<=1:
                        possible.append(y)
                    else:
                        break
            if len(possible)==1:
                my.put(row+1,possible[0],item)
                
        for item in left(my.get_column(row+1)):
            possible = list()
            #print(item)
            for y in free(my.get_column(row+1)):
                if (not item in my.get_row(y)):
                    #print(item," not in row ",y);
                    #input()
                    if len(possible)<=1:
                        possible.append(y)
                    else:
                        break
            if len(possible)==1:
                my.put(possible[0],row+1,item)

        '''        
        if num_left(my.get_row(row+1)) == 1 :
            #
            #print('\n',my.get_row(row+1),num_left(my.get_row(row+1)),sep='\t')
            #
            my.put(row+1,my.get_row(row+1).index(0)+1,left(my.get_row(row+1))[0])
        if num_left(my.get_column(row+1)) == 1 :
            #
            #print('\n',my.get_column(row+1),num_left(my.get_column(row+1)),sep='\t')
            #
            my.put(my.get_column(row+1).index(0)+1,row+1,left(my.get_column(row+1))[0])
        '''
        if num_left(my.get_chart(row+1)) == 1 :
            #
            #print('\n',my.get_chart(row+1),num_left(my.get_chart(row+1)),sep='\t')
            #
            not_fulled = my.free(row+1)[0]
            my.put(not_fulled[0]+1,not_fulled[1]+1,left(my.get_chart(row+1))[0])

        for cell in range(9):
            if my.grid[row][cell] != 0:
                chart_index = (((row )// 3)*3 + ((cell )// 3))+1
                #
                #print('\nnumber:',my.grid[row][cell],'chart index',chart_index,sep='\t')
                #
                charts = chartsinrow(chart_index)
                for x in charts:
                    #
                    #print('\nchart index in row',x,my.grid[row][cell] in my.get_chart(x),sep='\t')
                    #
                    if not my.grid[row][cell] in my.get_chart(x) :
                        can = list()
                        not_fulled = my.free(x)
                        #
                        #print('not fulled',not_fulled,sep='\t')
                        #
                        for i in not_fulled:
                            #print(f'not fulled {not_fulled.index(i)+1} row {my.get_row(i[0]+1)} column {my.get_column(i[1]+1)}')
                            if my.grid[row][cell] in my.get_row(i[0]+1) or my.grid[row][cell] in my.get_column(i[1]+1) :
                                #
                                #print(f'row {i[0]+1} and column {i[1]+1} contain {my.grid[row][cell]}')
                                #
                                pass
                                #not_fulled.remove(i)
                            else :
                                can.append(i)
                                #
                                #print(can)
                                #
                        if len(can) == 1 :
                            my.put(can[0][0]+1,can[0][1]+1,my.grid[row][cell])
                            #my.puts()
            #input('press to continue...')

end = time()-start
print(f'{int(end//60)} minute {str(end%60)[0:str(end%60).index(".")+3]} second ')





#row[index%3::3]
#row = my.get_row(1)
#column = my.get_column(9)
#chart = my.get_chart(5)

#print(row,column,chart,sep='\n\n')
