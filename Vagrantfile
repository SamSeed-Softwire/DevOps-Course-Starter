Vagrant.configure("2") do |config|
	config.vm.box = "hashicorp/bionic64"
  config.vm.network "forwarded_port", guest: 5000, host: 5000

  config.vm.provision "shell", privileged: false, inline:  <<-SHELL
    
    # Update all packages
    sudo apt-get update
    
    # Install pyenv prerequisites (taken from https://github.com/pyenv/pyenv/wiki/common-build-problems)
    sudo apt-get install -y build-essential libssl-dev zlib1g-dev libbz2-dev \
    libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev libncursesw5-dev \
    xz-utils tk-dev libffi-dev liblzma-dev python-openssl git
    
    # Install and configure pyenv
    sudo rm -r .pyenv
    sudo git clone https://github.com/pyenv/pyenv.git ~/.pyenv
    echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.profile
    echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.profile
    echo -e 'if command -v pyenv 1>/dev/null 2>&1; then\n  eval "$(sudo pyenv init -)"\nfi' >> ~/.profile
    cd .pyenv
    sudo mkdir shims
    sudo chmod 0777 shims
    sudo mkdir versions
    sudo chmod 0777 versions
    . ~/.profile
    
    # Install the desired version of python and set that version as the default version
    sudo pyenv install 3.8.5
    sudo pyenv global 3.8.5
    
    # Install poetry
    curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python

  SHELL

  config.trigger.after :up do |trigger|
    trigger.name = "Launching App"
    trigger.info = "Running the TODO app setup script"
    trigger.run_remote = {privileged: false, inline: "
        # Install dependencies and Launching
        cd /vagrant
        poetry install
        poetry run flask run --host=0.0.0.0
    "}
  end

end
