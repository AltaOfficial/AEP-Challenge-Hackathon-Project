use gtk::prelude::*;
use gtk::{glib, Application, ApplicationWindow, Box, Button, Label, Orientation, FileChooserAction, 
    FileChooserDialog, HeaderBar, ListBox, Paned, Stack, TextView, ActionBar};
//use matplotlib::Figure;

const APP_ID: &str = "com.AEP_AI_Dashboard.ui";

fn main() -> glib::ExitCode {
    let app = Application::builder().application_id(APP_ID).build();

    app.connect_activate(build_ui);

    app.run()
}

// top level box for two sided panes left side is diagram, right side are comments 
// make a box for diagram (pi chart histogram) unethe is a chat box with the option to look at
// comments 
// make a box or just item for input files
// 
//
// animations maybe


//  box
// -matplotlib
// -stack switcher or stack
//   -List box (comments)
//   -Vertical panes
//     -ActionBar (text)
//     -multiline text (output from ai)

// GtkFileChooserDialog (data dir location) https://stackoverflow.com/questions/29095970/gtkfilechooser-choose-only-directories
// GtkFileChooserDialog (Download data)
//

fn build_ui(app: &Application) {

    // Declare each widget
    // Putting the widgets together in a box
    let stack_comments_and_io = Stack::builder()
        .margin_top(12)
        .margin_bottom(12)
        .margin_start(12)
        .margin_end(12)
        .build();

    let list_comments = ListBox::builder()
        .margin_top(12)
        .margin_bottom(12)
        .margin_start(12)
        .margin_end(12)
        .build();
    let box_for_stack = Box::new(Orientation::Vertical, 0);
    box_for_stack.append(&stack_comments_and_io);
    box_for_stack.append(&list_comments);


    //let plot = false;
    let horizontal_pane = Paned::new(Orientation::Horizontal);
    let plot_and_stuff = Box::new(Orientation::Horizontal, 0);
    //plot_and_stuff.append(&plot);
    plot_and_stuff.append(&horizontal_pane);
    plot_and_stuff.append(&box_for_stack);

    
    let vertical_pane_io = Paned::new(Orientation::Vertical);
    let input_to_ai = ActionBar::builder()
        .margin_top(12)
        .margin_bottom(12)
        .margin_start(12)
        .margin_end(12)
        .build();
    let output_to_ai = TextView::builder()
        .margin_top(12)
        .margin_bottom(12)
        .margin_start(12)
        .margin_end(12)
        .build();
    let box_ai_io = Box::new(Orientation::Vertical, 0);
    box_ai_io.append(&input_to_ai);
    box_ai_io.append(&vertical_pane_io);
    box_ai_io.append(&output_to_ai);



    let dir_location = FileChooserAction::SelectFolder;
    let save_data_to = FileChooserAction::Save;

    // all the widgets in the GUI
    /*
    let label = Label::builder()
        .label("Balls and Cock")
        .margin_top(12)
        .margin_bottom(12)
        .margin_start(12)
        .margin_end(12)
        .build();

    let button = Button::builder()
        .label("Press me!")
        .margin_top(12)
        .margin_bottom(12)
        .margin_start(12)
        .margin_end(12)
        .build();
    */





    //let plot_box = create_plot();

    // Add views to the stack
    //stack.add_named(&comments_list, "Comments");
    //stack.add_named(&vertical_pane, "AI Output");
    //stack.add_named(&plot_box, "Plot");

    // Create buttons to switch between stack views
    //let button_box = Box::new(gtk::Orientation::Horizontal, 0);
    //button_box.pack_start(&create_switch_button("Comments", &stack, "Comments"), true, true, 0);
    //button_box.pack_start(&create_switch_button("AI Output", &stack, "AI Output"), true, true, 0);
    //button_box.pack_start(&create_switch_button("Plot", &stack, "Plot"), true, true, 0);
    //button_box.pack_start(&create_file_chooser_button(), true, true, 0);


    //




    // Pack everything into the main box
    let root = Box::new(Orientation::Vertical, 0);
    root.append(&plot_and_stuff);
    //root.append(&dir_location);
    //root.append(&save_data_to);

    let window = ApplicationWindow::builder()
        .application(app)
        .title("Dashboard")
        .child(&root)
        .build();
    window.set_default_size(800, 600);
    window.present();
}

fn plotStuff() {
    println!("need to implement");
}
