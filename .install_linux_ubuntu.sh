#sudo apt install git
#git clone potem login haslo
sudo apt -y install python3-pip
pip3 -y install pyqt5
pip3 -y install sip
sudo apt-get -y install --reinstall libxcb-xinerama0
python3 -m pip -y install pyautogui
sudo apt-get -y install python3-tk python3-dev
pip -y install opencv-python
pip -y install pynput
pip -y install youtube-search-python
pip -y install pytube
echo [daemon] | sudo tee -a /etc/gdm3/custom.conf
echo WaylandEnable=false | sudo tee -a /etc/gdm3/custom.conf
echo QT_QPA_PLATFORM=xcb | sudo tee -a /etc/environment
sudo apt-get -y install libgstreamer1.0-dev libgstreamer-plugins-base1.0-dev libgstreamer-plugins-bad1.0-dev gstreamer1.0-plugins-base gstreamer1.0-plugins-good gstreamer1.0-plugins-bad gstreamer1.0-plugins-ugly gstreamer1.0-libav gstreamer1.0-tools gstreamer1.0-x gstreamer1.0-alsa gstreamer1.0-gl gstreamer1.0-gtk3 gstreamer1.0-qt5 gstreamer1.0-pulseaudio
reboot
# pip3 install opencv-python3
# pip install opencv-python==4.5.3.5.6