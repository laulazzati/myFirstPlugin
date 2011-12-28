from gi.repository import GObject, Gtk, Gedit
import re

UI_XML = """<ui>
<menubar name="MenuBar">
    <menu name="ToolsMenu" action="Tools">
      <placeholder name="ToolsOps_3">
       <menu name="Submenu" action="SubmenuAction">
                <menuitem name="ExampleAction" action="ExampleAction2"/>
       </menu>
      </placeholder>
    </menu>
</menubar>
</ui>"""

class MyPlugin(GObject.Object, Gedit.WindowActivatable):
    __gtype_name__ = "WordMixer"
    window = GObject.property(type=Gedit.Window)
   
    def __init__(self):
        GObject.Object.__init__(self)
        
    
    def _add_ui(self):
        manager = self.window.get_ui_manager()
        self._actions = Gtk.ActionGroup("PerformAction")
        self._actions.add_actions([ ('SubmenuAction', Gtk.STOCK_INFO, "Submenu",None, "This is a submenu", None),
            ('ExampleAction2', Gtk.STOCK_INFO, "Mixer", 
                None, "Changes the order of the words of the document", 
                self.on_action_activate),
        ])
        manager.insert_action_group(self._actions)
        self._ui_merge_id = manager.add_ui_from_string(UI_XML)
        manager.ensure_update()
 
        
    def do_activate(self):
        self._add_ui()

    def do_deactivate(self):
        self._remove_ui()

    def do_update_state(self):
        pass
        

    def _mixer(self, viewBuffer):
        firstIter = viewBuffer.get_start_iter()
        nextIter = viewBuffer.get_start_iter()
        nextIter.forward_line()
       
        while firstIter.equal(viewBuffer.get_end_iter())<> True:
                textBuffer = viewBuffer.get_text(firstIter,nextIter,1)
                textList = re.split('\s',textBuffer)
                textList.reverse();
                newText = " ".join(textList)
                newText += "\n"
                viewBuffer.delete(firstIter, nextIter)
                viewBuffer.insert(firstIter, newText) 
                nextIter = firstIter.copy()
                nextIter.forward_line()  
                                   
                      
    
    def on_action_activate(self, action, data=None):
        view = self.window.get_active_view()
        if view:
            viewBuffer = view.get_buffer()
            self._mixer(viewBuffer)
            
 

                    
    def _remove_ui(self):
        manager = self.window.get_ui_manager()
        manager.remove_ui(self._ui_merge_id)
        manager.remove_action_group(self._actions)
        manager.ensure_update()
