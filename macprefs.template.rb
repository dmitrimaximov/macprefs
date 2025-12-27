class Macprefs < Formula
    desc "Backup and Restore your Mac System and App Preferences"
    homepage "https://github.com/clintmod/macprefs"
    url "https://github.com/clintmod/macprefs/archive/###version###.tar.gz"
    sha256 "###sha256###"

    depends_on "python@3"

    def install
      # Install the main script
      bin.install "macprefs"

      # Install Python modules to libexec
      libexec.install Dir["*.py"]
    end

    test do
      system "#{bin}/macprefs", "--help"
    end
  end
  