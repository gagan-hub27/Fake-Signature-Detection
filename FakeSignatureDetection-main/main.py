import tkinter as tk
from tkinter.filedialog import askopenfilename
from tkinter import messagebox
import os
import cv2
from skimage.metrics import structural_similarity as ssim
# If you have your original match function separate, you can import it; here we include an updated one
# THRESHOLD for match decision
THRESHOLD = 85

def list_available_cameras(max_index=10):
    available = []
    for i in range(max_index):
        cap = cv2.VideoCapture(i, cv2.CAP_DSHOW)
        if cap.isOpened():
            ret, _ = cap.read()
            if ret:
                available.append(i)
            cap.release()
    if not available:
        available = [0]
    return available

def match(path1, path2):
    img1 = cv2.imread(path1)
    img2 = cv2.imread(path2)
    if img1 is None or img2 is None:
        raise ValueError(f"Could not open one of the images: '{path1}' or '{path2}'")
    img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
    img1 = cv2.resize(img1, (300, 300))
    img2 = cv2.resize(img2, (300, 300))
    # Optional: comment out these lines if you don't want a popup window each time
    # cv2.imshow("One", img1)
    # cv2.imshow("Two", img2)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    similarity_value = float("{:.2f}".format(ssim(img1, img2) * 100))
    return similarity_value

def browsefunc(ent):
    filename = askopenfilename(filetypes=[
        ("image files", ".jpeg"),
        ("image files", ".png"),
        ("image files", ".jpg"),
    ])
    if filename:
        ent.delete(0, tk.END)
        ent.insert(tk.END, filename)

def capture_image_from_cam_into_temp(sign=1, cam_index=0):
    cam = cv2.VideoCapture(cam_index, cv2.CAP_DSHOW)
    if not cam.isOpened():
        messagebox.showerror("Camera Error", f"Cannot open camera index {cam_index}")
        return False
    cv2.namedWindow("Capture (Press SPACE to take picture, ESC to cancel)")
    while True:
        ret, frame = cam.read()
        if not ret:
            print("failed to grab frame")
            break
        cv2.imshow("Capture (Press SPACE to take picture, ESC to cancel)", frame)
        k = cv2.waitKey(1)
        if k % 256 == 27:  # ESC key
            print("Escape hit, closing...")
            break
        elif k % 256 == 32:  # SPACE key
            if not os.path.isdir('temp'):
                os.mkdir('temp', mode=0o777)
            fname = 'test_img1.png' if (sign == 1) else 'test_img2.png'
            img_name = os.path.join('temp', fname)
            cv2.imwrite(img_name, frame)
            print(f"{img_name} written!")
            break
    cam.release()
    cv2.destroyAllWindows()
    return True

def captureImage(ent, sign=1, cam_index=0):
    # Determine target filename (for display/entry)
    fname = 'test_img1.png' if (sign == 1) else 'test_img2.png'
    save_path = os.path.join(os.getcwd(), 'temp', fname)
    res = messagebox.askquestion(
        'Click Picture',
        'A window will open. Press SPACE to capture, ESC to cancel.'
    )
    if res == 'yes':
        ok = capture_image_from_cam_into_temp(sign=sign, cam_index=cam_index)
        if ok:
            ent.delete(0, tk.END)
            ent.insert(tk.END, save_path)
    return True

def checkSimilarity(window, path1, path2):
    try:
        result = match(path1=path1, path2=path2)
    except Exception as e:
        messagebox.showerror("Error", str(e))
        return False
    if result <= THRESHOLD:
        messagebox.showerror(
            "Failure: Signatures Do Not Match",
            f"Similarity = {result} %\nThreshold = {THRESHOLD}%"
        )
    else:
        messagebox.showinfo(
            "Success: Signatures Match",
            f"Similarity = {result} %\nThreshold = {THRESHOLD}%"
        )
    return True

# GUI Setup
root = tk.Tk()
root.title("Signature Matching")
root.geometry("500x700")

# Camera selection dropdown
camera_indices = list_available_cameras(10)
selected_cam = tk.IntVar(value=camera_indices[0])
tk.Label(root, text="Select Camera:", font=10).place(x=10, y=20)
tk.OptionMenu(root, selected_cam, *camera_indices).place(x=150, y=20)

tk.Label(root, text="Compare Two Signatures:", font=10).place(x=90, y=50)

# Signature 1
tk.Label(root, text="Signature 1", font=10).place(x=10, y=120)
image1_path_entry = tk.Entry(root, font=10, width=40)
image1_path_entry.place(x=150, y=120)
tk.Button(
    root, text="Capture", font=10,
    command=lambda: captureImage(ent=image1_path_entry, sign=1, cam_index=selected_cam.get())
).place(x=400, y=90)
tk.Button(
    root, text="Browse", font=10,
    command=lambda: browsefunc(ent=image1_path_entry)
).place(x=400, y=140)

# Signature 2
tk.Label(root, text="Signature 2", font=10).place(x=10, y=250)
image2_path_entry = tk.Entry(root, font=10, width=40)
image2_path_entry.place(x=150, y=240)
tk.Button(
    root, text="Capture", font=10,
    command=lambda: captureImage(ent=image2_path_entry, sign=2, cam_index=selected_cam.get())
).place(x=400, y=210)
tk.Button(
    root, text="Browse", font=10,
    command=lambda: browsefunc(ent=image2_path_entry)
).place(x=400, y=260)

# Compare button
tk.Button(
    root, text="Compare", font=10,
    command=lambda: checkSimilarity(
        window=root,
        path1=image1_path_entry.get(),
        path2=image2_path_entry.get()
    )
).place(x=200, y=320)

root.mainloop()
