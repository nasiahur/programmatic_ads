
class MonitorRouter(object):
    """
    A router to control all database operations on models in the
    monitor application.
    """
    def db_for_read(self, model, **hints):
        """
        Attempts to read monitor models go to monitor database.
        """
        if model._meta.db_table.startswith("monitor_"):
            return 'monitor'
        return None

    def db_for_write(self, model, **hints):
        """
        Attempts to write monitor models go to monitor database.
        """
        if model._meta.db_table.startswith("monitor_"):
            return 'monitor'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations if a model in the monitor app is involved.
        """
        if obj1._meta.db_table.startswith("monitor_") or obj2._meta.db_table.startswith("monitor_"):
            return True

        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Make sure the monitor app only appears in the 'monitor' 
        database.
        """
        if db == 'monitor':
            if app_label == "monitor":
                return True
            else:
                return False
        elif app_label == "monitor":
            return False
        return None
