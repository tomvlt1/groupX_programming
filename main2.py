from Dashboard import * 

def main():
    from Login import LoginGUI, AccountGUI 
    if getIDUser() == None:
        LoginGUI()
    else:              
        win = create_window()
        if not win:
            return

        buttons = create_sidebar(win)  # Now returns a dictionary
        overview_boxes = create_overview_section(win)
        refresh_button = RefreshButton(850, 60, win)

        mini_game_area, left, top, right, bottom = create_mini_game_area(win)
        preview_button, preview_text, lock_message = PreviewButton((left + right) // 2, (top + bottom) // 2, win)
        warning = WarningMessage((left + right) // 2, (top + bottom) // 2 + 60, win)

        mini_game_active = False

        while True:
            click = win.checkMouse()
            if click:
                # Preview button
                if not mini_game_active and is_click_in_rectangle(click, preview_button):
                    mini_game_active = True
                    preview_button.undraw()
                    preview_text.undraw()
                    lock_message.undraw()
                    warning.undraw()

                    FootGameHomeMain(win)

                    preview_button.draw(win)
                    preview_text.draw(win)
                    lock_message.draw(win)
                    warning.draw(win)
                    mini_game_active = False

                # Refresh button => Regenerate random facts
                elif is_click_in_rectangle(click, refresh_button):
                    new_facts = GetRandomFacts(3)
                    update_overview_section(win, overview_boxes, new_facts)

                # Import dataset
                elif is_click_in_rectangle(click, buttons.get("Import Dataset")):
                    userId = getIDUser()
                    if userId:
                        try:
                            # Use FileSelect.py's file_selector function
                            selected_file, selected_fileName= file_selector("target_folder",500,400)  
                            # Proceed to import the selected file into the database
                            print(selected_file)
                            result1, verror = check_csv_file(selected_file)
                            if result1:
                                result, last_insert_id, vmessage = create_load_record(userId,selected_fileName)
                                if result:
                                    result1, vmessage = import_csv_to_database(selected_file, int(userId), int(last_insert_id))
                                    if result1:
                                        messages(vmessage)
                                    else:
                                        messages(vmessage)
                                else:
                                    messages(verror)
                            else:
                                messages("Invalid CSV file.")
                        except FileNotFoundError as e:
                            messages(str(e))
                        except Exception as e:
                            messages(f"An error occurred: {str(e)}")

                # Visualize button

                # Profile button
                elif is_click_in_rectangle(click, buttons.get("Visualize Data")):
                    if getDataset() is None:
                        messages("Select Dataset")
                    else:
                        # Instead of run_visualize(), call build_filter_ui()
                        result_df = filtermain()  # or build_filter_ui() can also return a df
                        if result_df is not None:
                            print("Filtered DataFrame:", result_df)
                        # Possibly do something else with result_df

                # Import Dataset
                elif is_click_in_rectangle(click, buttons.get("Choose Dataset")):
                    userId = getIDUser()
                    if userId:
                        idload,vtxt=dataset_selector(320,600)
                        setDataset(idload) 
                        messages(f'your dataset for the study will be {vtxt}') 
                    
                # Other button logic...
                elif is_click_in_rectangle(click, buttons.get("FootClick Game")):
                    run_footclick()
                elif is_click_in_rectangle(click, buttons.get("Penalty game")):
                    run_headsoccer()
                elif is_click_in_rectangle(click, buttons.get("Back")):
                    session.clear
                    LoginGUI()
                elif is_click_in_rectangle(click, buttons.get("Main statistics")):
                    if getDataset() is None:
                        messages("Select Dataset")
                    else:
                        statistics(getIDUser())
                elif is_click_in_rectangle(click, buttons.get("Profile")):
                    AccountGUI(getIDUser())       
                # Visualize Data button
                

            time.sleep(0.05)

        win.close()


main()