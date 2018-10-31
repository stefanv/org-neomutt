;; Make sure org-protocol is loaded
(require org-protocol)

;; Call this function, which spawns neomutt, whenever org-mode
;; tries to open a link of the form mutt:message-id+goes_here@mail.gmail.com
;;
;; If using `maildir-utils` instead of `notmuch`, the search command becomes
;; `mu find -f l i:%s`.

(defun stefanv/mutt-open-message (message-id)
  "In neomutt, open the email with the the given Message-ID"
  (interactive)
  (let*
      ((mail-file
        (replace-regexp-in-string
         "\n$" "" (shell-command-to-string
                   (format "notmuch search --output=files id:%s" message-id))))
       (mail-dir (replace-regexp-in-string "/\\(cur\\|new\\|tmp\\)/$" ""
                                           (file-name-directory mail-file)))
       (process-id (concat "neomutt-" message-id))
       (message-id-escaped (regexp-quote message-id))
       (mutt-keystrokes
        (format "l~i %s\n\n" (shell-quote-argument message-id-escaped)))
       (mutt-command (list "neomutt" "-R" "-f" mail-dir
                           "-e" (format "push '%s'" mutt-keystrokes))))

    (message "Launching neomutt for message %s" message-id)
    (call-process "setsid" nil nil
                   "-f" "gnome-terminal" "--window" "--"
                   "neomutt" "-R" "-f" mail-dir
                   "-e" (format "push '%s'" mutt-keystrokes))))

;; Hook up `mutt:...` style URLs
(org-add-link-type "mutt" 'stefanv/mutt-open-message)
