# Flowshutter
# Copyright (C) 2021  Hugo Chiang

# Flowshutter is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# Flowshutter is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with flowshutter.  If not, see <https://www.gnu.org/licenses/>.
import vars, target
button_page, button_enter = target.init_buttons()


## globals
button_enter_prevstate = 0
button_enter_state = button_enter.value()
button_enter_press_count = 0

button_page_prevstate = 0
button_page_state = button_page.value()
button_page_press_count = 0
            
def check(t):
    global button_enter_prevstate
    global button_enter_state
    global button_enter_press_count

    global button_page_prevstate
    global button_page_state
    global button_page_press_count
    
    # load button states
    button_enter_prevstate = button_enter_state
    button_enter_state = button_enter.value()
    
    button_page_prevstate = button_page_state
    button_page_state = button_page.value()
    
    # enter button action
    if (button_enter_state != button_enter_prevstate): #detect button state change
        print("enter button state change")
        button_enter_press_count += 1
    
    if (button_enter_press_count//2 == 1 ): #only count button release
        button_enter_press_count = 0
        vars.button_enter = "pressed"
        print('button_enter ', vars.button_enter)


    # page button action
    if (button_page_state != button_page_prevstate): #detect button state change
        print("page button state change")
        button_page_press_count += 1
    
    if (button_page_press_count//2 == 1 ): #only count button release
        button_page_press_count = 0
        vars.button_page = "pressed"
        print('button_page ', vars.button_page)

    