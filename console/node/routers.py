
class NodeRouter(object):
    """
    A router to control all database operations on models in the
    node application.
    """
    def db_for_read(self, model, **hints):
        """
        Attempts to read node models go to node database.
        """
        if model._meta.db_table.startswith("node_"):
            return 'node'
        return None

    def db_for_write(self, model, **hints):
        """
        Attempts to write node models go to node database.
        """
        if model._meta.db_table.startswith("node_"):
            return 'node'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations if a model in the node app is involved.
        """
        if obj1._meta.db_table.startswith("node_") or obj2._meta.db_table.startswith("node_"):
            return True

        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Make sure the node app only appears in the 'node' 
        database.
        """
        if db == 'node':
            if app_label == "node":
                return True
            else:
                return False
        elif app_label == "node":
            return False
        return None
