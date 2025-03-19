# Install Checkmk Agent

Nach dem Herunterladen dieses Git-Projekts musst du die Agents im Verzeichnis  
`patchmgmt/checkmk_agent/packages` durch deine eigenen Agents ersetzen.  

Diese Agents werden verwendet, um Checkmk unter `/opt` zu installieren und die Plugins `yum` und `apt` bereitzustellen, die den Update-Status überwachen.

---

## Konfiguration anpassen

### Remote-User und SSH-Key ändern
Falls erforderlich, ändere den Remote-User oder füge einen SSH-Key hinzu:
```bash
vi /patchmgmt/patchmgmt/checkmk_agent/ansible.cfg
```

### Inventory anpassen
Öffne die Datei und füge die gewünschten Hosts hinzu:
```bash
vi /patchmgmt/patchmgmt/checkmk_agent/inventory.yml
```

**Beispiel-Inhalt für die Inventory-Datei:**
```ini
[Hostgroup]
host1.domain.com
```

---

## Playbook ausführen
Wenn du einen SSH-Key verwendest, kannst du die Option `-k` weglassen und stattdessen nur `-K` nutzen:

```bash
ansible-playbook -i inventory.yml playbook.yml -K
```

---

## Hinweise
- `-k` → Passwortabfrage für den SSH-Login  
- `-K` → Passwortabfrage für `sudo`  

Falls du weitere Anpassungen oder Erklärungen benötigst, lass es mich wissen! 🚀